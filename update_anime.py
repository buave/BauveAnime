import os

path_data = 'data/'
path_n_anime = 'data/n_anime/'
path_anime = 'anime/'
path_anime_html = 'anime_page/'

if not os.path.exists(path_n_anime):
    os.mkdir(path_n_anime)

os.system("ls -1 " + path_anime + " > " + path_data + "anime_list.txt")

p_index = open(path_data + "p_index.txt", "r")
for line in p_index:
    add_line = open("../index.html", "w")
    add_line.write(p_index.read())
    add_line.close()

tab_folder = os.popen("ls -l " + path_anime + " | wc -l")
list_folder = int(tab_folder.read())
anime_numb = list_folder - 1
f = open(path_data + "numb_anime.txt", "w")
f.write(str(anime_numb))
f.close()

list_new_anime = []
name_new_anime = open(path_data +"anime_list.txt", "r")
for line in name_new_anime:
    stripped_line = line.strip()
    if stripped_line != "":
        line_list = stripped_line.split()
        list_new_anime.append(str(line_list)[2:-2])
name_new_anime.close()

for name in list_new_anime:
    n_s = os.popen("ls " + path_anime + name)
    for s in n_s.readlines():
        if not os.path.exists(path_n_anime + name):
            os.mkdir(path_n_anime + name)
        n_ep = os.popen("ls " + path_anime + name + "/" + s[:-1] + " | wc -l" )
        numb_ep = open(path_n_anime + name + "/" + s[:-1] + ".txt", "w")
        numb_ep.write(n_ep.read())
        numb_ep.close()

for name_i in list_new_anime:
    saison = os.listdir(path_n_anime + name_i)
    for modif in saison:
        modif = modif[:-4]
        p_page = open(path_data + "p_page.txt", "r")
        add_html = open(path_data + "add_html.txt", "w")
        add_html.write("")
        add_html.close()
        for add in p_page.readlines():
            add_html = open(path_data + "add_html.txt", "a")
            add_html.write(str(add))
            add_html.close()
        with open(path_data + "add_html.txt", 'r+') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if line.startswith('<!--@EP@-->'):   # find a pattern so that we can add next to that line
                    n_ep = open(path_n_anime + name_i + "/" + modif + ".txt")
                    n_ep = int(n_ep.read()[:-1])
                    for option_ep in range(n_ep):
                        lines[i] = lines[i] + "<option value=" + str(option_ep + 1) + ">" + str(option_ep + 1) + "</option> \n"
            f.truncate()
            f.seek(0)                                       # rewrite into the file
            for line in lines:
                f.write(line)
        for option_sai in saison:
            option_sai = option_sai[:-4]
            with open(path_data + "add_html.txt", 'r+') as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    if line.startswith('<!--@SAI@-->'):   # find a pattern so that we can add next to that line
                        lines[i] = lines[i] + "<option value=" + option_sai + ">" + option_sai[-1:] + "</option> \n"
                f.truncate()
                f.seek(0)                                       # rewrite into the file
                for line in lines:
                    f.write(line)
        fin = open(path_data + "add_html.txt" , "rt")
        data = fin.read()
        name_modif = name_i.replace("_"," ")
        data = data.replace('ToChangeName', name_modif)
        data = data.replace('ToChange', name_i)
        fin.close()
        data = data.replace('ReplaceSaison', modif)
        EpMax = open(path_n_anime + name_i + "/" + modif + ".txt", 'r')
        data = data.replace("MaxEp", EpMax.read()[:-1])
        EpMax.close()
        fin = open(path_data + "add_html.txt", "wt")
        fin.write(data)
        fin.close()
        add_html = open(path_data + "add_html.txt", "r")
        if not os.path.exists(path_anime_html + name_i):
            os.mkdir(path_anime_html + name_i)
        html_anime = open(path_anime_html + name_i + "/" + name_i + "_" + modif + ".html", "w")
        html_anime.write(add_html.read())
        html_anime.close()

with open('../index.html', 'r+') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if line.startswith('<!--@SPF-JS-HEADER@-->'):   # find a pattern so that we can add next to that line
            for name in list_new_anime:
                with open(path_data + 'block_anime.txt') as myfile:
                    if name in myfile.read():
                        p_block_line = open(path_data + "p_block_line.txt", "r")
                        for line in p_block_line:
                            add_line = open(path_data + "add_line.txt", "w")
                            add_line.write(p_block_line.read())
                            name_modif = name.replace("_"," ")
                            line = line.replace('ToChangeName', name_modif)
                            add_line.write(line.replace('ToChange', name))
                            add_line.close()
                    else:
                        p_line = open(path_data +"p_line.txt", "r")
                        for line in p_line:
                            add_line = open(path_data + "add_line.txt", "w")
                            add_line.write(p_line.read())
                            name_modif = name.replace("_"," ")
                            line = line.replace("ToChangeName", name_modif)
                            add_line.write(line.replace('ToChange', name))
                            add_line.close()

                    add_line = open(path_data + "add_line.txt", "r")
                    lines[i] = lines[i] + add_line.read()

    f.truncate()
    f.seek(0)                                       # rewrite into the file
    for line in lines:
        f.write(line)

os.system("sudo rm ../script/indexA_script.js")
os.system("cp data/p_script.txt ../script/indexA_script.js")

with open('../script/indexA_script.js', 'r+') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if line.startswith('//HereAnime'):   # find a pattern so that we can add next to that line
            for name in list_new_anime:
                with open(path_data + 'block_anime.txt') as myfile:
                    if name in myfile.read():
                        pass
                    else:
                        name_modif = name.replace("_"," ")
                        add_line = f'"{name_modif}",'
                        lines[i] = lines[i] + add_line

        if line.startswith('//HereAllAnime'):   # find a pattern so that we can add next to that line
            for name in list_new_anime:
                name_modif = name.replace("_"," ")
                add_line = f'"{name_modif}",'
                lines[i] = lines[i] + add_line

    f.truncate()
    f.seek(0)                                       # rewrite into the file
    for line in lines:
        f.write(line)
