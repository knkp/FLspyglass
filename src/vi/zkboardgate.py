import datetime
import json
import time
import six
import requests
import logging
from bs4 import BeautifulSoup


class zKillBoard(object):
    def __init__(self, _char_name, _Cache, _gui_testing=False, _days=30):
        self.cache = _Cache
        self.days_of_killmail = _days
        self.character_name = _char_name
        self.CHAR_BASE_URL = 'https://zkillboard.com/search/'
        self.BASE_URL = 'https://zkillboard.com/api/'
        self.SHIP_BASE_URL = 'https://zkillboard.com/ship/'
        self.startTime = 0
        self.endTime = 0
        self.id = -1
        self.api_success = True
        self.user_found = True
        self.got_ships = True
        self.ships_unique = []
        self.ship_name_map = dict()
        self.ship_kills_occurence_map = dict()
        self.ship_loss_occurence_map = dict()
        self.kills_is_zero = False
        self.loss_is_zero = False

        if _gui_testing:
            self.ship_count = 10
            self.ships_unique = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            self.ship_name_map = dict()
            self.ship_name_map[1] = "Ishkur"
            self.ship_name_map[2] = "Kos"
            self.ship_name_map[3] = "blarg"
            self.ship_name_map[4] = "blarger"
            self.ship_name_map[5] = "blargerer"
            self.ship_name_map[6] = "blargerer"
            self.ship_name_map[7] = "blargerer"
            self.ship_name_map[8] = "blargerer"
            self.ship_name_map[9] = "blargerer"
            self.ship_name_map[10] = "blargerer"

            self.ship_kills_occurence_map[1] = 20
            self.ship_kills_occurence_map[2] = 7
            self.ship_kills_occurence_map[3] = 5
            self.ship_kills_occurence_map[4] = 5
            self.ship_kills_occurence_map[5] = 5
            self.ship_kills_occurence_map[6] = 5
            self.ship_kills_occurence_map[7] = 5
            self.ship_kills_occurence_map[8] = 5
            self.ship_kills_occurence_map[9] = 5
            self.ship_kills_occurence_map[10] = 5

            self.ship_loss_occurence_map[1] = 3
            self.ship_loss_occurence_map[2] = 15
            self.ship_loss_occurence_map[3] = 12
            self.ship_loss_occurence_map[4] = 12
            self.ship_loss_occurence_map[5] = 12
            self.ship_loss_occurence_map[6] = 12
            self.ship_loss_occurence_map[7] = 12
            self.ship_loss_occurence_map[8] = 12
            self.ship_loss_occurence_map[9] = 12
            self.ship_loss_occurence_map[10] = 12
        else:
            self.setTimeInterval(_days=self.days_of_killmail)
            self.getKillMail(self.character_name)
            self.orderShips()
            self.translateShipIds()

    def setTimeInterval(self, _days=30):
        delay = datetime.datetime.utcnow() - datetime.timedelta(days=_days)
        self.TIME = self.getTimeString(delay)

    def getTimeString(self, tm):
        result = str(tm.year)

        if len(str(tm.month)) > 1:
            result += str(tm.month)
        else:
            result += '0' + str(tm.month)

        if len(str(tm.day)) > 1:
            result += str(tm.day)
        else:
            result += '0' + str(tm.day)

        if len(str(tm.hour)) > 1:
            result += str(tm.hour)
        else:
            result += '0' + str(tm.hour)

        result += '00'

        return result

    def getCharId(self, name):
        import unicodedata
        name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
        name = name.lstrip(' ')
        self.id = self.cache.getFromCache(name)
        if self.id == None:
            try:
                url_redirect = requests.get(self.CHAR_BASE_URL + name + '/').url
                self.id = url_redirect.split('/')[-2]
            except Exception as e:
                logging.error("exception during getCharId for name: %s", name)
            self.cache.putIntoCache(name, self.id, 60*60*24*30)
        else:
            print 'got user ' + name + ' id from cache!'

    def getKillMail(self, name):
        self.getCharId(name)
       
        losses_url = self.BASE_URL + 'losses/characterID/' + \
            self.id + '/startTime/' + self.TIME + '/'
        kills_url = self.BASE_URL + 'kills/characterID/' + \
            self.id + '/startTime/' + self.TIME + '/'

        self.api_success = True
        self.losses = True
        self.kills = True
        if(id == -1):
            return
        else:
            try:
                self.losses_resp = requests.get(losses_url).json()
            except ValueError:
                logging.error(
                    "error occurred getting losses, we may have made too many requests")
                self.losses = False

            try:
                self.kills_resp = requests.get(kills_url).json()
            except ValueError:
                logging.error(
                    "error occurred getting kills, we may have made too many requests")
                self.kills = False

        if self.losses == False and self.kills == False:
            self.api_success = False

    def orderShips(self):
        # if self.losses_resp == None or self.kills_resp == None:
            self.ship_list_kills = []
            self.ship_list_losses = []

            if self.api_success == False or self.user_found == False:
                return

            # first collect all the losses ships id's and store each unique id separately
            if self.losses:    
                for obj in self.losses_resp:
                    if obj == unicode('error'):
                        self.user_found = False
                        return
                    ship_id = obj['victim']['ship_type_id']
                    if ship_id == 670:  # filter out the capsules
                        continue
                    try:
                        self.ships_unique.index(ship_id)
                    except:
                        self.ships_unique.append(ship_id)
                    self.ship_list_losses.append(ship_id)

            # next do the same with the kills
            if self.kills:  
                for obj in self.kills_resp:
                    for attacker in obj['attackers']:
                        ship_id = None
                        try:
                            if attacker[unicode('character_id')] == int(self.id):
                                ship_id = attacker[unicode('ship_type_id')]
                        except:
                            logging.error('attacker object format wrong')

                        if ship_id == None or ship_id == 670:
                            continue  # if we didn't get the ship id due to an exception or if it is a Capsule skip to the next iteration
                        try:
                            self.ships_unique.index(ship_id)
                        except:
                            self.ships_unique.append(ship_id)
                        self.ship_list_kills.append(ship_id)

            # By now we know how many unique ships there are, we need this number for the ui
            self.ship_count = len(self.ships_unique)

            # Now that we have organized the ship id's, we can count the occurences
            for ship_id in self.ships_unique:
                if self.losses:
                    loss_count = self.ship_list_losses.count(ship_id)
                    self.ship_loss_occurence_map[ship_id] = loss_count
                if self.kills:
                    kill_count = self.ship_list_kills.count(ship_id)
                    self.ship_kills_occurence_map[ship_id] = kill_count
                

            # Organize in ascending order the ship_id's based on the occurence count
            # Kills seem to be the primary interest (from what everyone has requested)
            new_list = []
            if self.kills: 
                for key, value in sorted(self.ship_kills_occurence_map.iteritems(), key=lambda (k, v): (v, k), reverse=True):
                    new_list.append(key)
            else:
                for key, value in sorted(self.ship_loss_occurence_map.iteritems(), key=lambda (k, v): (v, k), reverse=True):
                    new_list.append(key)

            self.ships_unique = new_list


    def translateShipIds(self):            
            if self.api_success == False or self.user_found == False:
                return

            for ship_id in self.ships_unique:
                ship_name = self.cache.getFromCache(ship_id)
                if ship_name == None:
                    url = self.SHIP_BASE_URL + str(ship_id) + '/'
                    try:
                        resp = requests.get(url).content
                    except:
                        logging.error("Error occurred getting ship data for ship_id: " + ship_id)
                        self.got_ships = False
                        return
                    soup = BeautifulSoup(resp, 'html.parser')
                    for a in soup.findAll('a'):
                        if a['href'] == unicode("/ship/" + str(ship_id) + '/'):
                            found = False
                            ship_name = 'none'
                            try:
                                ship_name = a['title']
                                found = True
                            except:
                                pass
                            if found:
                                self.ship_name_map[ship_id] = ship_name
                                self.cache.putIntoCache(ship_id, ship_name, 60*60*24*30)
                                continue
                else:
                    print 'got shipname ' + ship_name + ' from cache!'
                    self.ship_name_map[ship_id] = ship_name
                print 'ship names map: ' + str(self.ship_name_map)

                


            

        # else:
        #    logging.error("ordeShips responses are empty")

if __name__ == '__main__':
    test = zKillBoard('grimjack73', _gui_testing=True)
    # print test.character_name
    # for x in range(1,4):
    #    print test.ship_name_map[x] + ' : ' + str(test.ship_occurence_map[x])
    delay = datetime.datetime.utcnow() - datetime.timedelta(days=60)
    time = test.getTimeString(delay)
    # startTime = str(delay.year) + str(delay.month) + str(delay.day) + str(delay.hour) + str(delay.minute) + str(delay.second) + '00'
    # print startTime
    print time
