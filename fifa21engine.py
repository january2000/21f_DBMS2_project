from tkinter import *
from tkinter import messagebox
from tkinter.font import BOLD
import numpy

import mysql.connector

window = Tk()
window.title("FIFA 21")
window.geometry("1000x700")
import tkinter as tk
import tkinter.ttk
from tkcalendar import Calendar
from PIL import ImageTk, Image
import datetime

def clear():
    for widget in frame6.winfo_children():
        widget.destroy()

def getSQLDate(date):
    myDate = datetime.datetime.strptime(date, "%m/%d/%H")
    new_date = "20" + str(myDate.hour) + "-" + str(myDate.month) + "-" + str(myDate.day)
    return new_date

def search():
    filledCorrectly=True
    clear()
    whereStatement=True
    querySQL = str("SELECT playerprofile.id, short_name, nationality FROM playerprofile WHERE playerprofile.club_name LIKE '%%' ")
#PLAYER PROFILE PAGE

    if name_textbox.get()!="":
        querySQL = querySQL+" AND long_name LIKE '%"+name_textbox.get()+"%'"

    if age_textbox.get() !="":
        if age_textbox.get().isnumeric():
            if whereStatement:
                querySQL = querySQL+" AND age="+age_textbox.get()
        else:
            filledCorrectly=False
            messagebox.showerror("Error", "Wrong age")

    if height_textbox.get() !="":
        if height_textbox.get().isnumeric():
            if whereStatement:
                querySQL = querySQL+" AND height_cm="+height_textbox.get()
        else:
            filledCorrectly = False
            messagebox.showerror("Error", "Wrong height")

    if weight_textbox.get() !="":
        if weight_textbox.get().isnumeric():
            if whereStatement:
                querySQL = querySQL+" AND weight_kg>="+weight_textbox.get()
        else:
            filledCorrectly = False
            messagebox.showerror("Error", "Wrong weight")

    if nationality_combo.get()!="":
        if whereStatement:
            querySQL = querySQL + " AND nationality='"+nationality_combo.get()+"'"


#PLAYER CHARACTERISTICS PAGE
    join1Done=False
    if whereStatement: #LETS DO THE JOIN HERE
        join1Done=True
        querySQL = querySQL[0:67]+" join playercharacteristics pc on pc.id=playerprofile.id "+querySQL[67:]+" AND potential>=" + str(potential_scale.get()) + " AND pace>=" + str(pace_scale.get()) + " AND dribbling>=" + str(dribbling_scale.get()) + " AND defending>=" + str(defending_scale.get())+ " AND pace>=" + str(pace_scale.get()) + " AND physic>=" + str(physic_scale.get()) + " AND shooting>=" + str(shooting_scale.get()) + " AND goalkeeper>=" + str(gk_scale.get()) + " AND passing>=" + str(passing_scale.get())

    if foot_combo.get() != "":
        querySQL = querySQL + " AND preferred_foot='"+foot_combo.get()[0]+"'"

#PLAYER SPECIFICATIONS PAGE
    joinOnPlayerSpe= False
    if len(tp_combo.get()) != 0 or len(np_combo.get()) != 0 or len(njnum_textbox.get()) != 0:
        joinOnPlayerSpe = True
        querySQL = querySQL[0:124] + " join playerspecifications ps on pc.id=ps.id "+querySQL[124:]

        if len(tp_combo.get())!=0:
            querySQL = querySQL + " AND team_position='"+tp_combo.get()+"'"
        if len(np_combo.get())!=0:
            querySQL = querySQL + " AND nation_position='"+np_combo.get()+"'"
        if len(njnum_textbox.get())!=0:
            if njnum_textbox.get().isnumeric():
                querySQL = querySQL + " AND nation_jersey_number='"+njnum_textbox.get()+"'"
            else:
                filledCorrectly = False
                messagebox.showerror("Error", "Wrong nation jersey number")

# PLAYER CONTRACT PAGE

    if joinOnPlayerSpe:
        querySQL = querySQL[0:170] + " join playercontract pco on pc.id=pco.id " + querySQL[170:]+" AND value_eur>="+str(value_scale.get())+" AND wage_eur>="+str(wage_scale.get())+" AND release_clause_eur>="+str(rc_scale.get())+" AND join_date>="+str(join.get_date())+" AND contract_valid_until>="+str(cvu_scale.get())
    else:
        querySQL = querySQL[0:124] + " join playercontract pco on pc.id=pco.id " + querySQL[124:] + " AND value_eur>=" + str(value_scale.get()) + " AND wage_eur>=" + str(wage_scale.get()) + " AND release_clause_eur>=" + str(rc_scale.get()) + " AND join_date>=" + getSQLDate(join.get_date()) + " AND contract_valid_until>=" + str(cvu_scale.get())

#CLUB PAGE
    if len(cname_combo.get())!=0 or len(lname_combo.get())!=0 or len(lrank_textbox.get())!=0:
        if joinOnPlayerSpe:
            querySQL = querySQL[0:210] + " join teaminformation ti on ti.club_name=playerprofile.club_name " + querySQL[210:]
        else:
            querySQL = querySQL[0:164] + " join teaminformation ti on ti.club_name=playerprofile.club_name " + querySQL[164:]

        if len(cname_combo.get())!=0:
            querySQL = querySQL +" AND playerprofile.club_name='"+cname_combo.get()+"'"
        if len(lname_combo.get()) != 0:
            querySQL = querySQL + " AND league_name='" + lname_combo.get() + "'"
        if len(lrank_textbox.get())!=0:
            if lrank_textbox.get().isnumeric():
                querySQL = querySQL +" AND league_rank='"+lrank_textbox.get()+"'"
            else:
                filledCorrectly = False
                messagebox.showerror("Error", "Wrong league rank")

    print(querySQL)

    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="oscar0405",
        auth_plugin='mysql_native_password'
    )

    cursor = cnx.cursor()
    cursor.execute("USE footballplayersdb;")
    cursor.execute(querySQL+" LIMIT 10;")
    rows = cursor.fetchall()



    column_names = ["id", "name", "nationality", "update"]
    if len(rows)!=0:
        title_label = Label(frame6, width=20, text="Players")
        title_label.config(font=("Century Gothic", 13, BOLD))
        title_label.grid(row=0, column=1, columnspan=2, pady=5)

        for i in range(len(column_names)):
            columns_label = Label(frame6, width=10, text=column_names[i], font=("Century Gothic",11))
            columns_label.grid(row=1, column=i, pady=5)

        rentalids = numpy.zeros(len(rows))
        buttonsreturn = numpy.array([])

        i = 1
        for row in rows:
            i = i + 1
            rentalids[i - 2] = row[0]
            for j in range(len(row) + 1):
                if j == 3:
                    returnButton = Button(frame6, text="Return")
                    buttonsreturn = numpy.append(buttonsreturn, Button(frame6, text="Delete", font=("Arial", 8),
                                                                    command=lambda x=i - 2: deletefun(x)))
                    buttonsreturn[i - 2].grid(padx=25, pady=2, row=i, column=3)
                else:
                    e = Label(frame6, width=10, text=row[j], bg="white")
                    e.grid(padx=25, pady=2, row=i, column=j, ipadx=25)
                    e.config(font=("Arial", 8))
    else:
        text = "No players matching the characteristics :("
        noMatchingLabel = Label(frame6, text=text, bg="white")
        noMatchingLabel.grid(row=0, column=0, padx=160, pady=200)
        noMatchingLabel.config(font=("Arial", 20))

    def deletefun(rowNumber):
        cursor.execute(
            "DELETE FROM playerprofile WHERE id=" + str(int(rentalids[rowNumber])) + ";")
        cnx.commit()
        messagebox.showinfo("The player has been deleted !")
        search()

    if filledCorrectly:
        tkinter.messagebox.showinfo(title="searchDone", message="See the results in the results field !")

# background image
bg_image = ImageTk.PhotoImage(Image.open("background.jpg"))
bg_label = Label(window, image=bg_image)
bg_label.pack()

# logo image
logo_image = ImageTk.PhotoImage(Image.open("original.png"))
logo_label = Label(window, image=logo_image, bg="#524ddd")
logo_label.place(relx=0.5, rely=0.1, anchor=CENTER)

# tab style
s = tkinter.ttk.Style()
s.theme_create("MyStyle", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
        "TNotebook.Tab": {"configure": {"font" : ('Georgia Pro', '13', 'bold')},}})
s.theme_use("MyStyle")

# creating notebook
notebook = tkinter.ttk.Notebook(window, width=800, height=500)
notebook.place(relx=0.5, rely=0.58, anchor=CENTER)

# tab of player profile
tab1 = tkinter.Frame(window)
notebook.add(tab1, text="Player Profile")
frame1 = Frame(tab1, bg="white")
frame1.place(relwidth=1, relheight=1, relx=0, rely=0)

# name
name_label = Label(frame1, text="Player Name:", bg="white", font=("Century Gothic",12))
name_label.grid(row=0, column=0)

name = StringVar()
name_textbox = tkinter.ttk.Entry(frame1, width=22, textvariable=name, font=("Century Gothic", 9))
name_textbox.grid(row=0, column=1)

# age
age_label = Label(frame1, text="Age:", bg="white", font=("Century Gothic",12))
age_label.grid(row=1, column=0)

age = StringVar()
age_textbox = tkinter.ttk.Entry(frame1, width=22, textvariable=age, font=("Century Gothic", 9))
age_textbox.grid(row=1, column=1)

# height
height_label = Label(frame1, text="Height:", bg="white", font=("Century Gothic",12))
height_label.grid(row=2, column=0)

height = StringVar()
height_textbox = tkinter.ttk.Entry(frame1, width=22, textvariable=height, font=("Century Gothic", 9))
height_textbox.grid(row=2, column=1)

# weight
weight_label = Label(frame1, text="Weight:", bg="white", font=("Century Gothic",12))
weight_label.grid(row=3, column=0)

weight = StringVar()
weight_textbox = tkinter.ttk.Entry(frame1, width=22, textvariable=weight, font=("Century Gothic", 9))
weight_textbox.grid(row=3, column=1)

# nationality
nationality_label = Label(frame1, text="Nationality:", bg="white", font=("Century Gothic",12))
nationality_label.grid(row=4, column=0)

nationality = StringVar()
nationality_combo = tkinter.ttk.Combobox(frame1, height=5, width=20, textvariable=nationality, font=("Century Gothic", 9))
nationality_combo['values'] = ('Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Anguilla',
                               'Antigua And Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria',
                               'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium',
                               'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia And Herzegovina', 'Botswana',
                               'Bouvet Island', 'Brazil', 'British Virgin Islands', 'Brunei', 'Bulgaria',
                               'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde',
                               'Cayman Islands', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo',
                               'Cook Islands', 'Costa Rica', 'Croatia', 'Curacao', 'Cyprus', 'Czech Republic',
                               'Democratic Republic Of The Congo', 'Denmark', 'Djibouti', 'Dominica',
                               'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador',
                               'Equatorial Guinea', 'Estonia', 'Ethiopia', 'Faroe Islands', 'Fiji', 'Finland', 'France',
                               'French Guiana', 'French Polynesia', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana',
                               'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala',
                               'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hong Kong',
                               'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Isle Of Man',
                               'Israel', 'Italy', 'Ivory Coast', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan',
                               'Kenya', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho',
                               'Liberia', 'Libya', 'Libyan Arab Jamahiriya', 'Liechtenstein', 'Lithuania', 'Luxembourg',
                               'Macao', 'Macau', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali',
                               'Malta', 'Martinique', 'Mauritania', 'Mauritius', 'Mexico', 'Moldova', 'Monaco',
                               'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nepal',
                               'Netherlands', 'Netherlands Antilles', 'New Caledonia', 'New Zealand', 'Nicaragua',
                               'Niger', 'Nigeria', 'Norway', 'Oman', 'Pakistan', 'Palestine', 'Panama',
                               'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal',
                               'Puerto Rico', 'Qatar', 'Reunion', 'Romania', 'Russia', 'Russian Federation', 'Rwanda',
                               'Saint Kitts And Nevis', 'Saint Lucia', 'Saint Martin', 'Saint Pierre And Miquelon',
                               'Saint Vincent And The Grenadines', 'Samoa', 'San Marino', 'Saudi Arabia', 'Senegal',
                               'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Somalia',
                               'South Africa', 'South Korea', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname',
                               'Swaziland', 'Sweden', 'Switzerland', 'Taiwan', 'Tajikistan', 'Tanzania',
                               'Tanzania, United Republic Of', 'Thailand', 'Togo', 'Tonga', 'Trinidad And Tobago',
                               'Tunisia', 'Turkey', 'Turkmenistan', 'Turks And Caicos Islands', 'U.S. Virgin Islands',
                               'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States',
                               'Uruguay',
                               'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam', 'Wallis And Futuna', 'Yemen', 'Zambia',
                               'Zimbabwe')
nationality_combo.grid(row=4, column=1)


# search button
search_image_1 = ImageTk.PhotoImage(Image.open('search.jpg'))
search_button1 = Button(frame1, image=search_image_1, bg="white", command=search, borderwidth=0)
search_button1.grid(row=5, column=2, padx=20)

# tab of player characteristics
tab2 = tkinter.Frame(window)
notebook.add(tab2, text="Player Characteristics")
frame2 = Frame(tab2, bg="white")
frame2.place(relwidth=1, relheight=1, relx=0, rely=0)

# preferred foot
foot_label = Label(frame2, text="Preferred Foot:", bg="white", font=("Century Gothic",12))
foot_label.grid(row=0, column=0)

foot = StringVar()
foot_combo = tkinter.ttk.Combobox(frame2, height=5, width=23, textvariable=foot,font=("Century Gothic", 9))
foot_combo['values'] = ("Right", "Left")
foot_combo.grid(row=0, column=1)

# potential
potential_label = Label(frame2, text="Potential:", bg="white", font=("Century Gothic",12))
potential_label.grid(row=1, column=0)

potential = tkinter.StringVar()
potential_scale = tkinter.Scale(frame2, variable=potential, orient="horizontal", showvalue=True, tickinterval=10,
                                from_=45, to=100, length=170, bg="white", font=("Century Gothic", 9))
potential_scale.grid(row=1, column=1)

# pace
pace_label = Label(frame2, text="Pace:", bg="white", font=("Century Gothic",12))
pace_label.grid(row=2, column=0)

pace = tkinter.StringVar()
pace_scale = tkinter.Scale(frame2, variable=pace, orient="horizontal", showvalue=True, tickinterval=15,
                           from_=25, to=100, length=170, bg="white", font=("Century Gothic", 9))
pace_scale.grid(row=2, column=1)

# shooting
shooting_label = Label(frame2, text="Shooting:", bg="white", font=("Century Gothic",12))
shooting_label.grid(row=3, column=0)

shooting = tkinter.StringVar()
shooting_scale = tkinter.Scale(frame2, variable=shooting, orient="horizontal", showvalue=True, tickinterval=15,
                               from_=10, to=100, length=170, bg="white", font=("Century Gothic", 9))
shooting_scale.grid(row=3, column=1)

# passing
passing_label = Label(frame2, text="Passing:", bg="white", font=("Century Gothic",12))
passing_label.grid(row=4, column=0)

passing = tkinter.StringVar()
passing_scale = tkinter.Scale(frame2, variable=passing, orient="horizontal", showvalue=True, tickinterval=15,
                              from_=25, to=100, length=170, bg="white", font=("Century Gothic", 9))
passing_scale.grid(row=4, column=1)

# dribbling
dribbling_label = Label(frame2, text="Dribbling:", bg="white", font=("Century Gothic",12))
dribbling_label.grid(row=0, column=2)

dribbling = tkinter.StringVar()
dribbling_scale = tkinter.Scale(frame2, variable=dribbling, orient="horizontal", showvalue=True, tickinterval=15,
                                from_=25, to=100, length=170, bg="white", font=("Century Gothic", 9))
dribbling_scale.grid(row=0, column=3)

# defending
defending_label = Label(frame2, text="Defending:", bg="white", font=("Century Gothic",12))
defending_label.grid(row=1, column=2)

defending = tkinter.StringVar()
defending_scale = tkinter.Scale(frame2, variable=defending, orient="horizontal", showvalue=True, tickinterval=15,
                                from_=15, to=95, length=170, bg="white", font=("Century Gothic", 9))
defending_scale.grid(row=1, column=3)

# physic
physic_label = Label(frame2, text="Physic:", bg="white", font=("Century Gothic",12))
physic_label.grid(row=2, column=2)

physic = tkinter.StringVar()
physic_scale = tkinter.Scale(frame2, variable=physic, orient="horizontal", showvalue=True, tickinterval=15,
                             from_=25, to=100, length=170, bg="white", font=("Century Gothic", 9))
physic_scale.grid(row=2, column=3)

# goal keeper
gk_label = Label(frame2, text="Goal Keeper:", bg="white", font=("Century Gothic",12))
gk_label.grid(row=3, column=2)

gk = tkinter.StringVar()
gk_scale = tkinter.Scale(frame2, variable=gk, orient="horizontal", showvalue=True, tickinterval=10,
                         from_=0, to=60, length=170, bg="white", font=("Century Gothic", 9))
gk_scale.grid(row=3, column=3)

# overall
overall_label = Label(frame2, text="Overall:", bg="white", font=("Century Gothic",12))
overall_label.grid(row=4, column=2)

overall = tkinter.StringVar()
overall_scale = tkinter.Scale(frame2, variable=overall, orient="horizontal", showvalue=True, tickinterval=10,
                              from_=45, to=100, length=170, bg="white", font=("Century Gothic", 9))
overall_scale.grid(row=4, column=3)

# search button 2
search_image_2 = ImageTk.PhotoImage(Image.open('search.jpg'))
search_button2 = Button(frame2, image=search_image_2, bg="white", command=search, borderwidth=0)
search_button2.grid(row=5, column=4, padx=20)

# tab for player specification
tab3 = tkinter.Frame(window)
notebook.add(tab3, text="Player Specification")
frame3 = Frame(tab3, bg="white")
frame3.place(relwidth=1, relheight=1, relx=0, rely=0)


# team position
tp_label = Label(frame3, text="Team Position:", bg="white", font=("Century Gothic",12))
tp_label.grid(row=0, column=0)

tp = StringVar()
tp_combo = tkinter.ttk.Combobox(frame3, height=5, width=23, textvariable=tp, font=("Century Gothic", 9))
tp_combo['values'] = ('CAM', 'LS', 'ST', 'LW', 'RCM', 'LCB', 'RW', 'SUB', 'CF', 'CDM', 'RDM', 'RS', 'LCM', 'RB', 'LB',
                      'LM', 'RCB', 'LF', 'CB', 'RM', 'LDM', 'RF', 'RES', 'LWB', 'CM', 'LAM', 'RWB', 'RAM')
tp_combo.grid(row=0, column=1)

# nation position
np_label = Label(frame3, text="Nation Position:", bg="white", font=("Century Gothic",12))
np_label.grid(row=1, column=0)

np = StringVar()
np_combo = tkinter.ttk.Combobox(frame3, height=5, width=23, textvariable=np, font=("Century Gothic", 9))
np_combo['values'] = ('CAM', 'LS', 'ST', 'LW', 'RCM', 'LCB', 'RW', 'SUB', 'CF', 'CDM', 'RDM', 'RS', 'LCM', 'RB', 'LB',
                      'LM', 'RCB', 'LF', 'CB', 'RM', 'LDM', 'RF', 'RES', 'LWB', 'CM', 'LAM', 'RWB', 'RAM')
np_combo.grid(row=1, column=1)

# nation jersey number
njnum_label = Label(frame3, text="Nation Jersey Number:", bg="white", font=("Century Gothic",12))
njnum_label.grid(row=2, column=0)

njnum = StringVar()
njnum_textbox = tkinter.ttk.Entry(frame3, width=22, textvariable=njnum, font=("Century Gothic", 9))
njnum_textbox.grid(row=2, column=1)

# search button 3
search_image_3 = ImageTk.PhotoImage(Image.open('search.jpg'))
search_button3 = Button(frame3, image=search_image_3, bg="white", command=search, borderwidth=0)
search_button3.grid(row=2, column=2, padx=20)

# tab for contract
tab4 = tkinter.Frame(window)
notebook.add(tab4, text="Contract")
frame4 = Frame(tab4, bg="white")
frame4.place(relwidth=1, relheight=1, relx=0, rely=0)

# value
value_label = Label(frame4, text="Value (euro):", bg="white", font=("Century Gothic",12))
value_label.grid(row=0, column=0)

value = tkinter.IntVar()
value_scale = tkinter.Scale(frame4, variable=value, orient="horizontal", showvalue=True, tickinterval=105480000,
                            from_=20000, to=105500000, length=170, bg="white", font=("Century Gothic", 9))
value_scale.grid(row=0, column=1)

# wage
wage_label = Label(frame4, text="Wage (euro):", bg="white", font=("Century Gothic",12))
wage_label.grid(row=1, column=0)

wage = tkinter.IntVar()
wage_scale = tkinter.Scale(frame4, variable=wage, orient="horizontal", showvalue=True, tickinterval=559500,
                           from_=500, to=560000, length=170, bg="white", font=("Century Gothic", 9))
wage_scale.grid(row=1, column=1)

# release clause
rc_label = Label(frame4, text="Release Clause (euro):", bg="white", font=("Century Gothic",12))
rc_label.grid(row=2, column=0)

rc = tkinter.IntVar()
rc_scale = tkinter.Scale(frame4, variable=rc, orient="horizontal", showvalue=True, tickinterval=203069000,
                         from_=31000, to=203100000, length=170, bg="white", font=("Century Gothic", 9))
rc_scale.grid(row=2, column=1)

# join date
join_label = Label(frame4, text="Join Date:", bg="white", font=("Century Gothic",12))
join_label.grid(row=3, column=0)

join = Calendar(frame4, selectmode='day', background="white", foreground="black", font=("Century Gothic",9), selectbackground='dim grey')
join.grid(row=3, column=1)

# contract valid until
cvu_label = Label(frame4, text="Contract Valid Until (year):", bg="white", font=("Century Gothic",12))
cvu_label.grid(row=4, column=0)

cvu = tkinter.IntVar()
cvu_scale = tkinter.Scale(frame4, variable=cvu, orient="horizontal", showvalue=True, tickinterval=4,
                          from_=2020, to=2028, length=170, bg="white", font=("Century Gothic", 9))
cvu_scale.grid(row=4, column=1)

# search button 4
search_image_4 = ImageTk.PhotoImage(Image.open('search.jpg'))
search_button4 = Button(frame4, image=search_image_4, bg="white", command=search, borderwidth=0)
search_button4.grid(row=4, column=2, padx=20)

# tab for club
tab5 = tkinter.Frame(window)
notebook.add(tab5, text="Club")
frame5 = Frame(tab5, bg="white")
frame5.place(relwidth=1, relheight=1, relx=0, rely=0)

# club name
cname_label = Label(frame5, text="Club Name:", bg="white", font=("Century Gothic",12))
cname_label.grid(row=0, column=0)

cname = StringVar()
cname_combo = tkinter.ttk.Combobox(frame5, height=5, width=23, textvariable=cname, font=("Century Gothic", 9))
cname_combo['values'] = ('FC Barcelona', 'Juventus', 'FC Bayern München', 'Paris Saint-Germain', 'Manchester City',
                         'Liverpool', 'Real Madrid', 'Tottenham Hotspur', 'Napoli', 'Chelsea', 'Borussia Dortmund',
                         'Manchester United', 'Arsenal', 'Lazio', 'Atalanta', 'Real Sociedad', 'Leicester City',
                         'Inter',
                         'Olympique Lyonnais', 'Villarreal CF', 'Atlético Madrid', 'SL Benfica', 'Everton', 'FC Porto',
                         'Sevilla FC', 'RC Celta', 'AS Monaco', 'Wolverhampton Wanderers', 'Ajax', 'Valencia CF',
                         'Milan',
                         'Borussia Mönchengladbach', 'RB Leipzig', 'Real Betis', 'Inter Miami',
                         'Beijing Sinobo Guoan FC',
                         'Los Angeles FC', 'Al Shabab', 'Roma', 'Athletic Club de Bilbao',
                         'Guangzhou Evergrande Taobao FC',
                         'Shanghai SIPG FC', 'Crystal Palace', 'Bayer 04 Leverkusen', 'Medipol Başakşehir FK',
                         'Eintracht Frankfurt', 'Grêmio', 'Getafe CF', 'Olympique de Marseille', 'PFC CSKA Moscow',
                         'Leeds United', 'TSG 1899 Hoffenheim', 'West Ham United', 'Stade Rennais FC', 'Atlanta United',
                         'Vissel Kobe', 'Tigres U.A.N.L.', 'Fiorentina', 'Dalian YiFang FC', '1. FC Union Berlin',
                         'Shakhtar Donetsk', 'Boca Juniors', 'Sporting CP', 'Feyenoord', 'PSV', 'River Plate',
                         'VfL Wolfsburg',
                         'São Paulo', 'Atlético Mineiro', 'Palmeiras', 'Flamengo', 'Newcastle United', 'Dynamo Kyiv',
                         'Aston Villa', 'Torino', 'Levante UD', 'Watford', 'Burnley', 'Sassuolo', 'FC Groningen',
                         'Orlando City SC', 'Al Hilal', 'Sampdoria', 'Guangzhou R&F FC', 'Galatasaray SK',
                         'Jiangsu Suning FC',
                         'West Bromwich Albion', 'Al Nassr', 'Fenerbahçe SK', 'Beşiktaş JK', 'LOSC Lille',
                         'Southampton',
                         'Lokomotiv Moscow', 'Fluminense', 'Sheffield United', 'SV Werder Bremen', 'OGC Nice',
                         'SC Freiburg',
                         'CA Osasuna', 'FC Schalke 04', 'SC Braga', 'Vitória Guimarães', 'Estudiantes de La Plata',
                         'FC Girondins de Bordeaux', 'Olympiacos CFP', 'Portland Timbers', 'SD Eibar', 'Racing Club',
                         'Girona FC', 'Shanghai Greenland Shenhua FC', 'Real Valladolid CF', 'Montpellier HSC',
                         'Cagliari',
                         'Deportivo Alavés', 'Toronto FC', 'RC Strasbourg Alsace', 'Coritiba', 'Santos', 'Hertha BSC',
                         'AZ Alkmaar', 'RCD Espanyol', 'Spartak Moscow', 'Granada CF', 'Brighton & Hove Albion',
                         'BSC Young Boys', 'Cruz Azul', 'AS Saint-Étienne', 'Parma', 'Genoa', 'San Lorenzo de Almagro',
                         'Royal Antwerp FC', 'Club Atlético Lanús', 'Seattle Sounders FC', 'Monterrey', 'FC Nantes',
                         'Club Brugge KV', 'SK Slavia Praha', 'Wuhan Zall', 'FC Augsburg', 'Sivasspor', 'Club León',
                         'Internacional', 'Trabzonspor', 'Norwich City', 'Fulham', 'Stade de Reims', 'Bournemouth',
                         'Dinamo Zagreb', 'Brentford', '1. FC Köln', 'Udinese', 'Celtic', 'Derby County',
                         'Fatih Karagümrük S.K.',
                         'En Avant de Guingamp', 'LA Galaxy', 'Shijiazhuang Ever Bright F.C.', 'Hellas Verona',
                         'CD Leganés',
                         'Qingdao Huanghai F.C.', 'Birmingham City', 'Tianjin TEDA FC', 'Bologna',
                         'Universidad Católica',
                         'Vélez Sarsfield', 'Independiente', 'Al Ahli', 'Goiás', 'Alanyaspor', 'FC Red Bull Salzburg',
                         '1. FSV Mainz 05', 'KRC Genk', 'Racing Club de Lens', 'FC Metz', 'Rio Ave FC', 'FC Utrecht',
                         'FC Midtjylland', 'Aalborg BK', 'AEK Athens', 'Olimpia Asunción', 'FC Basel 1893', 'Junior FC',
                         'Hamburger SV', 'Santos Laguna', 'Cádiz CF', 'Perth Glory', 'Deportivo Toluca', 'Rosenborg BK',
                         'FC København', 'KAA Gent', 'Swansea City', 'Çaykur Rizespor', 'Angers SCO',
                         'Chongqing Dangdai Lifan FC SWM Team',
                         'RCD Mallorca', 'Montreal Impact', 'New England Revolution', 'Real Zaragoza',
                         'DSC Arminia Bielefeld',
                         'Al Wehda', 'Pachuca', 'Stade Malherbe Caen', 'Al Ain FC', 'Godoy Cruz', 'SPAL', 'Colo-Colo',
                         'Columbus Crew SC',
                         'Vasco da Gama', 'Botafogo', 'Fortaleza', 'Guadalajara', 'Famalicão', 'Portimonense SC',
                         'VfB Stuttgart',
                         'Club América', 'SC Heerenveen', 'Rangers FC', 'Nîmes Olympique', 'Boavista FC', 'U.N.A.M.',
                         'Atlético Nacional',
                         'Preston North End', 'Toulouse Football Club', 'Dijon FCO', 'Defensa y Justicia',
                         'Real Salt Lake',
                         'SD Huesca', 'New York Red Bulls', 'Moreirense FC', 'New York City FC', 'Millwall',
                         'Stade Brestois 29',
                         'Vancouver Whitecaps FC', 'FC Lorient', 'Antalyaspor', 'Molde FK', 'PAOK', 'Western United FC',
                         'Shandong Luneng TaiShan FC', 'Wisła Kraków', 'Denizlispor', "Newell's Old Boys",
                         'Nacional de Montevideo', 'Malmö FF', 'Henan Jianye FC', 'Fortuna Düsseldorf', 'Sparta Praha',
                         'Kayserispor', 'SV Sandhausen', 'Benevento', 'Minnesota United FC', 'Houston Dynamo',
                         'Rosario Central', 'Club Atlético Colón', 'FC Seoul', 'Paris FC', 'MKE Ankaragücü',
                         'Al Taawoun', 'FC Dallas', 'Atlético de San Luis', 'Elche CF', 'Club Tijuana',
                         'Argentinos Juniors', 'Independiente del Valle', 'Chicago Fire', 'Amiens SC', 'Deportivo Cali',
                         'Yeni Malatyaspor', 'VfL Bochum 1848', 'Clube Sport Marítimo', 'Kaizer Chiefs',
                         'Panathinaikos FC', 'Nottingham Forest', 'Astra Giurgiu', 'Daegu FC', 'Bahia',
                         'Atlético Clube Goianiense', 'Club Athletico Paranaense', 'Club Atlético Talleres',
                         'FCSB (Steaua)', '1. FC Nürnberg', 'Sporting de Charleroi', 'Standard de Liège',
                         'Viktoria Plzeň', 'Reading', 'UD Almería', 'Shenzhen FC', 'FC St. Gallen', 'Blackburn Rovers',
                         'San Jose Earthquakes', 'Kashiwa Reysol', 'LASK Linz', 'Vitesse', 'Club Libertad', 'Willem II',
                         'Club Guaraní', 'DC United', 'FC Sion', 'Al Ittihad', 'Gençlerbirliği SK', 'KAS Eupen',
                         'Rayo Vallecano', 'Göztepe SK', 'Western Sydney Wanderers', 'Sporting Kansas City',
                         'ESTAC Troyes', 'Sydney FC', 'Jeonbuk Hyundai Motors', 'FC Juárez', 'Ettifaq FC',
                         'Yokohama F. Marinos', 'Club Atlas', 'Club Atlético Aldosivi', 'Orlando Pirates',
                         'RSC Anderlecht', 'Holstein Kiel', 'Atiker Konyaspor', 'Unión de Santa Fe', 'Gil Vicente FC',
                         'Club Atlético Banfield', 'Sint-Truidense VV', 'Huddersfield Town', 'Real Oviedo',
                         'CD Tondela', 'América de Cali', 'Middlesbrough', 'FC Emmen', 'SK Rapid Wien', 'Hammarby IF',
                         'FK Bodø/Glimt', 'AD Alcorcón', 'Colorado Rapids', 'Philadelphia Union', 'Al Faisaly',
                         'Peñarol', 'Nashville SC', '1. FC Heidenheim 1846', 'Gamba Osaka', 'Melbourne City FC',
                         'Millonarios FC', 'Puebla FC', 'Wolfsberger AC', 'Ulsan Hyundai FC', 'Mazatlán FC', 'AIK',
                         'FK Austria Wien', 'River Plate Asunción', 'Os Belenenses', 'Crotone', 'Hatayspor', 'CFR Cluj',
                         'Sheffield Wednesday', 'Stoke City', 'Cardiff City', 'AC Monza', 'Kawasaki Frontale',
                         'Brescia', 'FC Tokyo', 'Servette FC', 'Universitatea Craiova', 'Gimnasia y Esgrima La Plata',
                         'Independiente Medellín', 'Ceará Sporting Club', 'Gazişehir Gaziantep F.K.', 'Club Necaxa',
                         'Real Sporting de Gijón', 'Club Atlético Huracán', 'Bristol City', 'Hannover 96',
                         'Queens Park Rangers', 'FC Paços de Ferreira', 'SC Paderborn 07', 'Legia Warszawa',
                         'Santa Clara', 'KV Kortrijk', 'CD Tenerife', 'Hebei China Fortune FC', 'Farense',
                         'KV Mechelen', 'Hokkaido Consadole Sapporo', 'Querétaro', 'FC Cincinnati', 'Raków Częstochowa',
                         'Kasimpaşa SK', 'Lech Poznań', 'LDU Quito', 'CD Nacional', 'BB Erzurumspor', 'Helsingborgs IF',
                         'Lecce', '1. FC Kaiserslautern', 'IFK Göteborg', 'Central Córdoba', 'Atlético Tucumán',
                         'Dinamo Bucureşti', 'Wellington Phoenix', 'SV Darmstadt 98', 'Chievo Verona', 'Djurgårdens IF',
                         'Spezia', 'AJ Auxerre', 'FC Erzgebirge Aue', 'Al Fateh', 'ADO Den Haag', 'El Nacional',
                         'Nagoya Grampus', 'Al Fayha', 'Piast Gliwice', 'SV Zulte-Waregem', 'Damac FC',
                         'Deportivo Binacional', 'Kashima Antlers', 'Al Hazem', 'Patronato', 'Cerezo Osaka',
                         'Oceânico FC', 'Barnsley', 'CF Fuenlabrada', 'IFK Norrköping', 'Adelaide United',
                         'SD Ponferradina', 'Heracles Almelo', 'FC Ingolstadt 04', 'Shamrock Rovers',
                         'Sanfrecce Hiroshima', 'Brøndby IF', 'SpVgg Greuther Fürth', 'FC St. Pauli', 'SK Sturm Graz',
                         'Emelec', 'Hull City', 'Albacete BP', 'KSV Cercle Brugge', 'Aarhus GF', 'Beerschot AC',
                         'UD Las Palmas', 'Málaga CF', 'Clermont Foot 63', 'FC Viitorul', 'GwangJu FC',
                         'Coquimbo Unido', 'FC Cartagena', 'Arsenal de Sarandí', 'Empoli', 'AC Ajaccio', 'CD Lugo',
                         'FC Nordsjælland', 'Karlsruher SC', 'IF Elfsborg', 'SG Dynamo Dresden', 'Royal Excel Mouscron',
                         'Shimizu S-Pulse', 'HJK Helsinki', 'Vålerenga Fotball', 'Jagiellonia Białystok', 'Al Raed',
                         'FC Luzern', 'Aberdeen', 'Barcelona Sporting Club', 'Coventry City', 'Doncaster Rovers',
                         'Chamois Niortais Football Club', 'VVV-Venlo', 'Urawa Red Diamonds', 'Suwon Samsung Bluewings',
                         'Abha Club', 'Oud-Heverlee Leuven', 'Oita Trinita', 'FC Lugano', 'Dundalk',
                         'Club Atlético Tigre', 'Valenciennes FC', 'VfL Osnabrück', 'PEC Zwolle', 'Górnik Zabrze',
                         'Pohang Steelers', 'Sunderland', 'Kilmarnock', 'Shonan Bellmare', 'Le Havre AC', 'SK Brann',
                         'Grenoble Foot 38', 'Fortuna Sittard', 'Melbourne Victory', 'FC Twente', 'Luton Town',
                         'SSV Jahn Regensburg', 'La Berrichonne de Châteauroux', 'Cusco FC', 'Unión La Calera',
                         'Pogoń Szczecin', 'Śląsk Wrocław', 'BK Häcken', 'Club Bolívar', 'Liverpool Fútbol Club',
                         'Zagłębie Lubin', 'Gangwon FC', 'FC Zürich', 'Alianza Lima', 'Eintracht Braunschweig',
                         'Sol de América', 'Incheon United FC', 'Nacional Asunción', 'Cracovia', 'Melgar FBC',
                         'Oriente Petrolero', 'Universidad Católica del Ecuador', 'Motherwell', 'Odense Boldklub',
                         'Stabæk Fotball', 'KV Oostende', 'SV Wehen Wiesbaden', 'Portsmouth', 'UD Logroñés',
                         'Sparta Rotterdam', 'Sepsi OSK', 'Wigan Athletic', 'Audax Italiano', 'Lechia Gdańsk',
                         'Charlton Athletic', 'Viking FK', 'Rodez Aveyron Football', 'FC Sochaux-Montbéliard',
                         'MSV Duisburg', 'River Plate Montevideo', 'Milton Keynes Dons', 'SCR Altach', 'Lincoln City',
                         'Lyngby BK', 'Oxford United', 'Wycombe Wanderers', 'C.D. Castellón', 'AS Nancy Lorraine',
                         'Vegalta Sendai', 'Hibernian', 'TSV Hartberg', 'Deportivo Pasto', 'Delfín SC', 'FC Voluntari',
                         'Always Ready', 'Jorge Wilstermann', 'Kristiansund BK', 'FC Botoşani', 'FC Chambly Oise',
                         'SD Aucas', 'Nacional Potosí', 'Odds BK', 'St. Johnstone FC', 'SV Waldhof Mannheim',
                         'CE Sabadell FC', 'Newcastle Jets', 'CD Huachipato', 'Hallescher FC', 'Waasland-Beveren',
                         'IK Sirius', 'Peterborough United', 'Vejle Boldklub', 'Rotherham United', 'Gaz Metan Mediaş',
                         'FC Hansa Rostock', 'Pau FC', 'WSG Tirol', 'Ipswich Town', 'IK Start', 'Kalmar FF',
                         'FC Würzburger Kickers', 'Sarpsborg 08 FF', 'Livingston FC', 'SpVgg Unterhaching',
                         'St. Mirren', 'Fleetwood Town', 'FC Lausanne-Sport', 'Sagan Tosu', 'TSV 1860 München',
                         'SV Ried', 'Busan IPark', 'Stal Mielec', 'SønderjyskE', 'Centro Atlético Fénix', 'Wisła Płock',
                         'SV Meppen', 'Estudiantes de Mérida', 'Sport Huancayo', 'CD Mirandés', 'Crewe Alexandra',
                         'Blackpool', 'Club Plaza Colonia', 'Aalesunds FK', 'Club Atlético Grau', 'FK Haugesund',
                         'Plymouth Argyle', 'Bristol Rovers', 'FSV Zwickau', 'RKC Waalwijk', 'AC Horsens',
                         'Viktoria Köln', 'Politehnica Iaşi', 'Salford City', 'FC Hermannstadt', 'Randers FC',
                         'KFC Uerdingen 05', 'Warta Poznań', 'Northampton Town', 'Burton Albion', 'Al Adalah',
                         'Seongnam FC', 'AC Mineros de Guayana', 'Örebro SK', 'USL Dunkerque', 'Sportivo Luqueño',
                         'UTA Arad', 'Chindia Târgovişte', 'Caracas FC', 'Bayern München II', 'Strømsgodset IF',
                         'Southend United', 'FC Admira Wacker Mödling', 'Exeter City', 'Gillingham',
                         'Hamilton Academical FC', 'Bradford City', 'Rochdale', 'Yokohama FC', 'Forest Green Rovers',
                         'Dundee United', 'SKN St. Pölten', 'Shrewsbury', 'FC Argeș', 'Türkgücü München',
                         'Sangju Sangmu FC', '1. FC Magdeburg', 'Cambridge United', 'Swindon Town', 'Carlisle United',
                         'Port Vale', 'Tranmere Rovers', 'Colchester United', 'Bolton Wanderers', 'Macarthur FC',
                         'VfB Lübeck', 'Brisbane Roar', 'Accrington Stanley', 'Cheltenham Town', 'FC Vaduz',
                         '1. FC Saarbrücken', 'Mjällby AIF', 'Academica Clinceni', 'Aragua FC', 'Club Blooming',
                         'Barrow', 'Central Coast Mariners', 'SC Verl', 'Ross County FC', 'Östersunds FK',
                         'Newport County', 'Sandefjord Fotball', 'Mansfield Town', 'Crawley Town', 'AFC Wimbledon',
                         'Falkenbergs FF', 'Mjøndalen IF', 'Varbergs BoIS', 'Walsall', 'Oldham Athletic',
                         'Scunthorpe United', 'Leyton Orient', 'Grimsby Town', 'Stevenage',
                         'Podbeskidzie Bielsko-Biała', 'Morecambe', 'Bohemian FC', 'Derry City', 'Llaneros de Guanare',
                         'Sligo Rovers', 'Cork City', "St. Patrick's Athletic", 'Zamora FC', 'Shelbourne FC',
                         'Harrogate Town', 'Waterford FC', 'Finn Harps')
cname_combo.grid(row=0, column=1)

# league name
lname_label = Label(frame5, text="League Name:", bg="white", font=("Century Gothic",12))
lname_label.grid(row=1, column=0)

lname = StringVar()
lname_combo = tkinter.ttk.Combobox(frame5, height=5, width=23, textvariable=lname, font=("Century Gothic", 9))
lname_combo['values'] = (
    'Spain Primera Division', 'Italian Serie A', 'German 1. Bundesliga', 'French Ligue 1', 'English Premier League',
    'Portuguese Liga ZON SAGRES', 'Holland Eredivisie', 'USA Major League Soccer', 'Chinese Super League',
    'Saudi Abdul L. Jameel League', 'Turkish Süper Lig', 'Campeonato Brasileiro Série A', 'Russian Premier League',
    'Japanese J. League Division 1', 'Mexican Liga MX', 'Ukrainian Premier League', 'Argentina Primera División',
    'English League Championship', 'Greek Super League', 'Spanish Segunda División', 'Swiss Super League',
    'Belgian Jupiler Pro League', 'Czech Republic Gambrinus Liga', 'Croatian Prva HNL', 'Scottish Premiership',
    'French Ligue 2', 'Chilian Campeonato Nacional', 'Austrian Football Bundesliga', 'Danish Superliga',
    'Paraguayan Primera División', 'Colombian Liga Postobón', 'German 2. Bundesliga', 'Australian Hyundai A-League',
    'Norwegian Eliteserien', 'UAE Arabian Gulf League', 'Italian Serie B', 'Polish T-Mobile Ekstraklasa',
    'Uruguayan Primera División', 'Swedish Allsvenskan', 'Korean K League Classic', 'Ecuadorian Serie A',
    'South African Premier Division', 'Romanian Liga I', 'German 3. Bundesliga', 'Peruvian Primera División',
    'Rep. Ireland Airtricity League', 'English League One', 'Finnish Veikkausliiga', 'Argentinian Primera B Nacional',
    'Liga de Fútbol Profesional Boliviano', 'Venezuelan Primera División', 'English League Two')
lname_combo.grid(row=1, column=1)

# league rank
lrank_label = Label(frame5, text="League Rank:", bg="white", font=("Century Gothic",12))
lrank_label.grid(row=2, column=0)

lrank = tkinter.StringVar()
lrank_textbox = tkinter.ttk.Entry(frame5, width=22, textvariable=lrank, font=("Century Gothic", 9))
lrank_textbox.grid(row=2, column=1)

# search button 5
search_image_5 = ImageTk.PhotoImage(Image.open('search.jpg'))
search_button5 = Button(frame5, image=search_image_4, bg="white", command=search, borderwidth=0)
search_button5.grid(row=2, column=2, padx=20)

# tab of player characteristics
tab6 = tkinter.Frame(window)
notebook.add(tab6, text="Results")
frame6 = Frame(tab6, bg="white")
frame6.place(relwidth=1, relheight=1, relx=0, rely=0)

window.mainloop()