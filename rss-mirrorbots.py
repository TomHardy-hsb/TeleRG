import feedparser
import schedule
import datetime
import time
from telethon import TelegramClient, events, sync
api_id = APIIDHERE
api_hash = 'APIHASHHERE'
client = TelegramClient('rssbot-session', api_id, api_hash)
client.start()

#Pre-definitions

def time_current(repeatInterval_duration):
    
    time_now = datetime.datetime.now()

    second_c = time_now.second
    minute_c = time_now.minute - repeatInterval_duration
    hour_c = time_now.hour
    day_c = time_now.day
    month_c = time_now.month
    year_c = time_now.year
    
    
    if time_now.second < 0:
        second_c = 60 + time_now.second
        minute_c = time_now.minute - 1 
    if time_now.minute - repeatInterval_duration < 0:
        minute_c = 60 + time_now.minute - repeatInterval_duration
        hour_c = time_now.hour - 1
        if hour_c < 0:
            hour_c = 23
            day_c = time_now.day - 1
            if day_c <= 0:
                if time_now.month == 1 or 5 or 7 or 10 or 12:
                    day_c = 30
                if time_now.month == 2 or 4 or 6 or 8 or 9 or 11:
                    day_c = 31
                if time_now.month == 3:
                    if ((time_now.year)/4) == 0:
                            day_c = 29
                    if ((time_now.year)/4) != 0:
                            day_c = 28
                month_c = time_now.month - 1
                if month_c <= 0:
                    year_c = time_now.year - 1

    return (datetime.datetime(year_c, month_c, day_c, hour_c, minute_c, second_c))

def time_magnet(feedPublishing_time):
    
    i = 0
            
    day_v = ''
    month_v = ''
    year_v = ''
    hour_v = ''
    minute_v = ''
    second_v = ''
    timezone_h = ''
    timezone_m = ''
    
    for c in feedPublishing_time:
        i += 1
        if i >= 6 and i <= 7:
            day_v += c
        if i >= 9 and i <= 11:
            month_v += c
        if i >= 13 and i <= 16:
            year_v += c
        if i >= 18 and i <= 19:
            hour_v += c
        if i >= 21 and i <= 22:
            minute_v += c
        if i >= 24 and i <= 25:
            second_v += c
        if i == 27:
            forb = c
        if i >= 28 and i <= 29:
            timezone_h += c
        if i >= 30 and i <= 31:
            timezone_m += c

 
    
    if  month_v == 'Jan':
        month_v = 1
    if  month_v == 'Feb':
        month_v = 2
    if  month_v == 'Mar':
        month_v = 3
    if  month_v == 'Apr':
        month_v = 4
    if  month_v == 'May':
        month_v = 5
    if  month_v == 'Jun':
        month_v = 6
    if  month_v == 'Jul':
        month_v = 7
    if  month_v == 'Aug':
        month_v = 8
    if  month_v == 'Sep':
        month_v = 9
    if  month_v == 'Oct':
        month_v = 10
    if  month_v == 'Nov':
        month_v = 11
    if  month_v == 'Dec':
        month_v = 12
    
    if forb == '+':
        sign = 1
    if forb == '-':
        sign = -1
    
    day_v = int(day_v)
    year_v = int(year_v)
    hour_v = int(hour_v) - (int(timezone_h) * sign)
    minute_v = int(minute_v) - (int(timezone_m) * sign)
    second_v = int(second_v)

    if minute_v < 0:
        minute_v = 60 + minute_v
        hour_v = hour_v - 1
    if hour_v < 0:
        hour_v = 24 + hour_v
        day_v = day_v - 1
        if day_v <= 0:
            if month_v == 1 or 5 or 7 or 10 or 12:
                day_v = 30
            if month_v == 2 or 4 or 6 or 8 or 9 or 11:
                day_v = 31
            if month_v == 3:
                if ((year_v)/4) == 0:
                        day_v = 29
                if ((year_v)/4) != 0:
                        day_v = 28
            month_v = month_v - 1
            if month_v <= 0:
                year_v = year_v - 1
    
    if minute_v > 59:
        minute_v = minute_v - 60
        hour_v = hour_v + 1
    if hour_v > 23:
        hour_v = hour_v - 24
        day_v = day_v + 1
        if month_v == 1 or 5 or 7 or 10 or 12:
            if day_v > 31:
                day_v = 1
        if month_v == 2 or 4 or 6 or 8 or 9 or 11:
            if day_v > 30:
                day_v = 1
        if month_v == 3:
            if ((year_v)/4) == 0:
                    if day_v > 29:
                        day_v = 1
            if ((year_v)/4) != 0:
                    if day_v > 28:
                        day_v = 1

    return (datetime.datetime(year_v, month_v, day_v, hour_v, minute_v, second_v))

def isTitleExcluded(entry, title_exclusions, include):
    for i in title_exclusions:
        if i in entry.title:
            if include:
                return False
            print ("Name Check Failed | " + entry.title)
            return True
    if include:
        print ("Name Check Failed | " + entry.title)
        return True
    return False

def main(url_rss, repeat, entity, botusername, title_exclusions, include):

    rss_feed = feedparser.parse(url_rss)
    
    for c in range (len(rss_feed.entries)):

        entry = rss_feed.entries[c]

        if time_magnet(entry.published) > time_current(repeat):
            print ("Time Check Passed | " + entry.title)
            if not isTitleExcluded(entry, title_exclusions, include):    
                print ("Name Check Passed | " + entry.title)
                client.parse_mode = 'html'    
                client.send_message(entity, "<b>/mirror@" 
                                    + botusername 
                                    + "</b> <code>" + entry.link 
                                    + "</code> <b>\n\nName: </b><code>" +  entry.title 
                                    + "</code><b>\nPublished: </b><code>" + entry.published 
                                    + '</code>\n\ncc: YOURUSERNAME')
        else:
            print ("Time Check Failed | " + entry.title)

#User-definitions

def fnc1():
    main(   
        "RSSLINK", 
         REPEATINTERVALINMINUTES,
        -GROUPID,
        "MIRRORBOTUSERNAME",
        [FILTER1,FILTER2],
        INCLUDE
        )


fnc1()

schedule.every(30).minutes.do(fnc1)

while True: 
  
    schedule.run_pending() 
    time.sleep(1)
