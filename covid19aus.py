#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.
# Riza Azmi (University of Wollongong, Australia)

import logging
import telegram
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [['1', '2', '3'],
                  ['4', '5', '6'],
                  ['7', '8', '9'],
                  ['🏠']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

reply_keyboard3 = [['1', '2', '3'],
                  ['4', '5', '6'],
                  ['7', '8', '9'],
                  ['🏠']]
markup3 = ReplyKeyboardMarkup(reply_keyboard3, one_time_keyboard=False)

reply_keyboard2 = [['🏠'],['DONE']]
markup2 = ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True)

def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(update, context):
    update.message.reply_text(
        "*Welcome to the Australian Government's Telegram Bot Channel for guidance & information on Australia's response to Coronavirus (COVID-19).*\n\n"
        "We treat your privacy on this channel seriously. To read about our privacy policy reply *99*.\n\n"
        "Reply with number or emoji to get more information:\n\n"
        "*1* 🗞 Latest news\n"
        "*2* 🔢 Latest numbers\n"
        "*3* 🌡 Check your symptoms\n"
        "*4* 😷 Protect yourself & others\n"
        "*5* 👨‍👩‍👧‍👦 Support for people & families\n"
        "*6* 💼 Support for businesses\n"
        "*7* 🗺 Travel advice\n"
        "*8* 🛣Advice from states & territories\n"
        "*9* ⏩ Share this Telegram Bot\n\n"
        "*What would you like information on? For example, reply '1' or 🗞 to see the latest news.*",
        reply_markup=markup, parse_mode=telegram.ParseMode.MARKDOWN)
        
    return CHOOSING


def regular_choice(update, context):
    x = update.message.text.upper()
    context.user_data['choice'] = x
    if x == '1':
        update.message.reply_text("*1. 🗞 NEWS*\n\n"
        "- *Self isolating?* \n- If you are in self-isolation because you are confirmed or suspected to have Coronavirus, or have been in close contact with a confirmed case, use this form to help us track the spread of the virus → aus.gov.au/covid-form\n\n"
        "- *Safety net* \n- A safety net package of $1.1 billion has been announced by the Prime Minister to expand mental health and telehealth services, increase domestic violence services and provide more emergency food relief.\n\n"
        "- *Stay informed* \n- Download the “Coronavirus Australia” government app in the Apple App Store and on Google Play.\n\n"
        "- *Travel* \n- All travellers returning home from overseas will be quarantined in a hotel or designated facility for 14 days.\n\n"
        "- *Travel* \n- Interstate travellers should return to and stay at home.\n\n"
        "- *Centrelink* \n- Register your intention to claim using mygov aus.gov.au/intent-to-claim\n\n"
        "- *Restrictions* \n- Check State & Territory websites for closures and social distancing rules in public spaces, gatherings and businesses such as restaurants cinemas, sporting venues, salons and more.\n\n"
        "*Stop the spread!*\n"
        "Stay 1.5 metres away from others, wash your hands regularly for at least 20 seconds with soap and water, avoid touching your face and if sick, stay home.\n\n"
        "More? Read → aus.gov.au/news\n\n"
        "_Reply_ *8* _or 🛣 for State & Territory information_, *0* _or 🏠 for Main menu_"        
        ,reply_markup=markup3,parse_mode=telegram.ParseMode.MARKDOWN)
    elif x == '2':
        mes = "*Confirmed Cases*\n\n"
        try:
            from urllib.request import urlopen
            html = urlopen("https://www.health.gov.au/news/health-alerts/novel-coronavirus-2019-ncov-health-alert/coronavirus-covid-19-current-situation-and-case-numbers?utm_source=Telegram&utm_medium=Social&utm_campaign=@COVID19AUS_BOT").read()
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            i = 1
            j = 1
            for s in soup.find('table').find_all('td'):
                if s.text.strip() != '':
                    if i%2 == 1:
                        mes += (str(j) if (j<9) else '') + '. ' + s.text.strip().replace("*","†").strip() + ' '
                        j += 1
                    else:
                        mes += '*' + s.text.strip().replace("*","†").strip() + '*\n'
                i += 1                
            mes += "View more data & statistics → aus.gov.au/current-numbers\n\nReply 0 or 🏠 for Main menu."
        except Exception as e:
            mes = "View more the numbers → aus.gov.au/current-numbers\n\n_Reply_ *0* _or 🏠 for Main menu_."
        update.message.reply_text(mes,reply_markup=markup2,parse_mode=telegram.ParseMode.MARKDOWN)
    elif x == '3':
        update.message.reply_text(
            "*3. 🤒 CHECK YOUR SYMPTOMS*\n\n"
            "*Common symptoms of COVID-19 include:*\n\n"
            " - coughing\n"
            " - fatigue\n"
            " - fever\n"
            " - shortness of breath\n"
            " - sore throat\n\n"
            "*Online symptom checker*\n"
            "You can also use the Coronavirus (COVID-19) Symptom checker → aus.gov.au/symptom-checker\n\n"
            "*Have symptoms?*\n"
            "If you are sick & think you have symptoms, book an appointment to seek medical advice.\n"
            "Find your nearest health centre → aus.gov.au/health-services\n\n"
            "The doctor will tell you if you should be tested. They will arrange for a test if needed.\n\n"
            "*If you are having a medical emergency call 000.*\n\n"
            "_Reply_ *0* _or 🏠 for Main menu_",reply_markup=markup2,parse_mode=telegram.ParseMode.MARKDOWN)
    elif x == '4':
        update.message.reply_text(
            "*4. 😷 PROTECT YOURSELF & OTHERS*\n\n"
            "*Everyone MUST practice good hygiene*. It protects against infection & prevents the virus spreading.\n"
            "🤧 Cover your coughs & sneezes with your elbow or a tissue\n"
            "🚮 Put used tissues straight into the bin\n"
            "🧼 Wash your hands often with soap & water (including before & after eating & after going to the toilet)\n"
            "✅ Use alcohol-based hand sanitisers\n"
            "😷 Avoid touching your eyes, nose & mouth\n\n"
            "*You MUST also practice:*\n"
            "- Social distancing → aus.gov.au/social-distancing\n"
            "- Limits on public gatherings → aus.gov.au/public-gatherings\n"
            "- Self-isolation (self-quarantine) → aus.gov.au/self-isolation (where necessary)\n\n"
            "*Cleaning*\n"
            "🧹 Clean & disinfect frequently used surfaces such as benchtops, desks & doorknobs\n"
            "📱 Clean & disinfect frequently used objects such as mobile phones, keys, wallets & work passes\n"
            "🌬 Increase fresh air available by opening windows or adjusting air conditioning\n\n"
            "_Reply_ *0* _or 🏠 for Main menu_",reply_markup=markup2,parse_mode=telegram.ParseMode.MARKDOWN)
    elif x == '5':
        update.message.reply_text(
            "*5. 👨‍👩‍👧‍👦 SUPPORT FOR PEOPLE & FAMILIES*\n\n"
            "If your work has been impacted by Coronavirus the new JobKeeper payment may help. → aus.gov.au/jobkeeper\n\n"
            "If you're affected by coronavirus, Services Australia can help with information and services for:\n"
            "Carers →  aus.gov.au/carers\n"
            "Families →  aus.gov.au/families\n"
            "Indigenous Australians → aus.gov.au/indigenous\n"
            "Job seekers → aus.gov.au/job-seekers\n"
            "Older Australians → aus.gov.au/older-australians\n"
            "People with disability → aus.gov.au/disability\n"
            "Rural and remote residents → aus.gov.au/rural-remote\n"
            "Students and trainees → aus.gov.au/students-trainees\n"
            "If you haven't received a payment → aus.gov.au/you-dont-receive-payment\n\n"
            "*Mental health and other support*\n"
            "Get support and advice for:\n"
            "Mental health → aus.gov.au/headtohealth\n"
            "Family and domestic violence → aus.gov.au/family-domestic-violence\n\n"
            "_Reply_ *0* _or 🏠 for Main menu_",reply_markup=markup2,parse_mode=telegram.ParseMode.MARKDOWN)
    elif x == '6':
        update.message.reply_text(
            "*6. 💼 SUPPORT FOR BUSINESSES*\n\n"
            "If your business has been significantly impacted by Coronavirus find out how to access the JobKeeper payment. → aus.gov.au/jobkeeper\n\n"
            "If you need support for your business and employees, you can find information including financial assistance, eligibility & timing for government support by going to:\n"
            "aus.gov.au/support-for-business\n\n"
            "_Reply *0* or 🏠 for Main menu_",reply_markup=markup2,parse_mode=telegram.ParseMode.MARKDOWN)
    elif x == '7':
        update.message.reply_text(
            "*7. 🗺 TRAVEL\n\n*"
            "*🌏 International*\n"
            "An international travel ban is in place for all Australians.\n\n"
            "All travellers to Australia or Australians returning from overseas are required to quarantine for 14 days in a hotel or designated facility.\n\n"            
            "*🦘 Within Australia*\n"
            "Only essential travel within Australia should occur at this time. TAS, NT, WA, QLD & SA border closures. Anyone entering these states or territories are required to self-isolate for 14 days. \n\n"           
            "*Self-isolating?*\n"
            "For information on how to self-isolate (self-quarantine) go to → aus.gov.au/self-isolation\n\n"
            "_Reply_ *8* _or 🛣 for State & Territory advice_, *0* _or 🏠 for Main menu_",reply_markup=markup3,parse_mode=telegram.ParseMode.MARKDOWN)
    elif x == '8':
        update.message.reply_text(
            "*8. 🛣 ADVICE FROM STATES & TERRITORIES*\n\n"
            "States & territories provide advice on the status of services like education, public transport, parks & other recreational areas.\n\n"
            "_Click the link below for your state to get local information_\n\n"
            "*ACT* → aus.gov.au/covid19-act\n"
            "*NSW* → aus.gov.au/covid19-nsw\n"
            "*NT* → aus.gov.au/covid19-nt\n"
            "*QLD* → aus.gov.au/covid19-qld\n"
            "*SA* → aus.gov.au/covid19-sa\n"
            "*TAS* → aus.gov.au/covid19-tas\n"
            "*VIC* → aus.gov.au/covid19-vic\n"
            "*WA* → aus.gov.au/covid19-wa\n\n"
            "_Reply_ *2* _or 🔢 for Latest numbers by State & Territory_, *0* _or 🏠 for Main menu_",reply_markup=markup3,parse_mode=telegram.ParseMode.MARKDOWN)
    elif x == '9':
        update.message.reply_text(
            "9. ⏩ SHARE THIS TELEGRAM BOT\n\n"
            "Protect yourself, your family, friends and community.\n\n"
            "Copy this link and share:  \n\n"
            "Reply 0 or 🏠 for Main menu",reply_markup=markup2,parse_mode=telegram.ParseMode.MARKDOWN)
    elif x == '99':
        update.message.reply_text(
            "*99. PRIVACY STATEMENT*\n\n"
            "Your telephone number will be collected and stored by the Digital Transformation Agency (DTA) when you use this service. No other personal information will be collected. Your number will not be used or disclosed for any other purpose. When you navigate around the app, information about the sites visited will be recorded but will not be linked to your telephone number. If you select a link that sends you to a website of another agency or organisation, you should read the privacy policy of that agency or organisation.\n\n" 
            "Further information about the DTA’s privacy practices → www.dta.gov.au/our-privacy-policy\n\n"
            "_If you agree to this use reply_ *0* _or 🏠 to return to the main menu_.",reply_markup=markup2,parse_mode=telegram.ParseMode.MARKDOWN)
    elif x == 'DONE':
        update.message.reply_text(
            "*THANK YOU*\n\n"
            "Thank you for using this service.\n\n"
            "Type /start if you want to restart conversation.",reply_markup=markup2,parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        update.message.reply_text(
            "_Reply_ *0* _or 🏠 for Main menu_. \n\nType /start if you want to restart conversation.",reply_markup=markup2,parse_mode=telegram.ParseMode.MARKDOWN)
    return CHOOSING

def done(update, context):
    update.message.reply_text("Terimakasih!")
    user_data.clear()
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater("INSERTTOKENHERE", use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [MessageHandler(Filters.regex('^(1|2|3|4|5|6|7|8|9|DONE|99)$'),
                                      regular_choice),
                       MessageHandler(Filters.text,
                                      start)
                       ],

        },

        fallbacks=[MessageHandler(Filters.regex('^DONE$'), done)]
    )  
    dp.add_handler(conv_handler)
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
