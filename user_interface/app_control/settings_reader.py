import os

def setting_grab(setting):
    #Opening File
    file= open(r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control\settings.txt", "r")
    contents = file.readlines()
    settings = []

    #Spliting the lines at point with = character
    for line in contents:
        if(line.find('=') == -1):
            continue
        settings.extend(line.split("="))

    #Finding setting's results
    try:
        elem = settings.index(setting)
        if(settings[elem + 1] == '\n'):
            return "None"

        #Optaining the information of the setting and spliting it from the title
        list = settings[elem + 1]

        if(list.find(',') > 0):
            #For multiple address settings
            #Spliting the multiple addresses
            list = list.split(',')

            #Removing the \n character at the end
            last_element = list[-1]
            last_element_cut = last_element[0:-1]
            list[list.index(last_element)] = last_element_cut

            #Converting String to raw literal string
            for element in list:
                eval_element = eval(element)
                list[list.index(element)] = eval_element
                #"%r"%eval_element
            return list

        else:
            #For single address settings
            #removing \n at the end of the string
            list = list[0:-1]
            #Cleaning the string
            list = eval(list)
            return list

    except ValueError:
        raise RuntimeError("Invalid Setting Title")

complete_path = os.path.dirname(os.path.abspath(__file__))
skore_index = complete_path.find('SKORE') + len('SKORE')
skore_path = complete_path[0:skore_index+1]

#templates_address =[r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control\audiveris_automation\templates",
#                    r"C:\Users\daval\Documents\GitHub\SKORE\user_interface\app_control\xenoplay_automation\templates"]

#print(templates_address)

#list = setting_grab('templates_address')
#print(list)

#list2 = setting_grab('user_input_address_audi')
#print(list2)
#print(list[0])
