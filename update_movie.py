import os

path_data = 'data/'
path_n_movie = 'data/n_movie/'
path_movie = 'movie/'
path_movie_html = 'movie_page/'

if not os.path.exists(path_n_movie):
    os.mkdir(path_n_movie)

os.system("ls -1 " + path_movie + " > " + path_data + "movie_list.txt")

p_index = open(path_data + "p_index.txt", "r")
for line in p_index:
    add_line = open("../index_movie.html", "w")
    add_line.write(p_index.read())
    add_line.close()

tab_folder = os.popen("ls -l " + path_movie + " | wc -l")
list_folder = int(tab_folder.read())
movie_numb = list_folder - 1
f = open(path_data + "numb_movie.txt", "w")
f.write(str(movie_numb))
f.close()

list_new_movie = []
name_new_movie = open(path_data +"movie_list.txt", "r")
for line in name_new_movie:
    stripped_line = line.strip()
    if stripped_line != "":
        line_list = stripped_line.split()
        list_new_movie.append(str(line_list)[2:-2])
name_new_movie.close()

for name_i in list_new_movie:
    p_page = open(path_data + "p_page.txt", "r")
    add_html = open(path_data + "add_html.txt", "w")
    add_html.write("")
    add_html.close()
    for add in p_page.readlines():
        add_html = open(path_data + "add_html.txt", "a")
        add_html.write(str(add))
        add_html.close()
    fin = open(path_data + "add_html.txt" , "rt")
    data = fin.read()
    name_modif = name_i.replace("_"," ")
    data = data.replace('ToChangeName', name_modif)
    data = data.replace('ToChange', name_i)
    fin.close()
    fin = open(path_data + "add_html.txt", "wt")
    fin.write(data)
    fin.close()
    add_html = open(path_data + "add_html.txt", "r")
    if not os.path.exists(path_movie_html + name_i):
        os.mkdir(path_movie_html + name_i)
    html_movie = open(path_movie_html + name_i + "/" + name_i + "_movie.html", "w")
    html_movie.write(add_html.read())
    html_movie.close()

with open('../index_movie.html', 'r+') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if line.startswith('<!--@SPF-JS-HEADER@-->'):   # find a pattern so that we can add next to that line
            for name in list_new_movie:
                with open(path_data + 'block_movie.txt') as myfile:
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

os.system("sudo rm ../script/indexM_script.js")
os.system("cp data/p_script.txt ../script/indexM_script.js")

with open('../script/indexM_script.js', 'r+') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if line.startswith('//HereAnime'):   # find a pattern so that we can add next to that line
            for name in list_new_movie:
                with open(path_data + 'block_movie.txt') as myfile:
                    if name in myfile.read():
                        pass
                    else:
                        name_modif = name.replace("_"," ")
                        add_line = f'"{name_modif}",'
                        lines[i] = lines[i] + add_line

        if line.startswith('//HereAllAnime'):   # find a pattern so that we can add next to that line
            for name in list_new_movie:
                name_modif = name.replace("_"," ")
                add_line = f'"{name_modif}",'
                lines[i] = lines[i] + add_line

    f.truncate()
    f.seek(0)                                       # rewrite into the file
    for line in lines:
        f.write(line)

# with open('../script/indexM_script.js', 'r+') as f:
#     lines = f.readlines()
#     lines = lines[:-2]
#     with open('../script/indexM_script.js', 'w') as a:
#         for line in lines:
#             a.write(line)
#         a.close()
