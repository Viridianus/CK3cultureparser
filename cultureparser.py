labels = "culture;" + ";".join(sorted(["created","ethos","ethnicities","heritage","color","language","parents","name_list",
"traditions","martial_custom","coa_gfx","building_gfx","clothing_gfx","unit_gfx"]))# + ';tribe\n'
print("Enter file name; enter empty string to finish")
filename = input().strip()
cultures = []
has_tribes = False
while filename != "":
	try:
		with open(filename, 'r') as fr:
			not_in_culture = True
			curr = []
			in_subpart = False
			subpart_name = ""
			content = ""
			curr_culture = ""
			curr_subpart_names = []
			for line in fr:
				l = line.split('#',1)[0].strip()
				if l == "":
					continue
				if not_in_culture:
					if l[-1] == "{": #should always be True but seemingly isn't
						curr_culture = l.split("=",1)[0].rstrip()
						#curr.append(l)
						not_in_culture = False
					else:
						continue
				elif l == "}":
					if in_subpart:
						in_subpart = False
						if subpart_name == "dlc_tradition":
							subpart_name = ""
							content = ""
							continue #ain't dealing with that shit
						elif subpart_name in curr_subpart_names:
							tmp = list(filter(lambda x: x[:len(subpart_name)] == subpart_name, curr))[0]
							curr.remove(tmp)
							curr.append(tmp + " " + content.strip())
						else:
							curr.append(subpart_name + ":" + content[:-1])
							curr_subpart_names.append(subpart_name)
						subpart_name = ""
						content = ""
					else:
						not_in_culture = True
						curr.sort()
						curr_culture = curr_culture + ";" + ";".join(curr) + '\n'
						if "color" not in curr_culture:
							curr_culture = curr_culture.replace("_coa_gfx;","coa_gfx;;")
						if "created" not in curr_culture:
							curr_culture = curr_culture.replace(";ethnicities:",";;")
						else:
							curr_culture = curr_culture.replace(";ethnicities:",";").replace("created:","")
						if "parents" not in curr_culture:
							curr_culture = curr_culture.replace(";traditions:",";;")
						else:
							curr_culture = curr_culture.replace(";traditions:",";")
						for sn in curr_subpart_names:
							curr_culture = curr_culture.replace(sn + ":","")
						if " tribe" in curr_culture:
							has_tribes = True
							curr_culture = curr_culture.replace(" tribe",";tribe")
						cultures.append(curr_culture)#.replace(" tribe",";tribe"))
						curr = []
						curr_culture = ""
						curr_subpart_names = []
				elif l[-1] == "}":
					subpart_name, content = l[:-1].split('{', 1)
					if subpart_name == "color = rgb ":
						subpart_name = "color"
					else:
						subpart_name = subpart_name.rstrip()[:-2]
					if subpart_name in curr_subpart_names:
						tmp = list(filter(lambda x: x[:len(subpart_name)] == subpart_name, curr))[0]
						curr.remove(tmp)
						curr.append(tmp + " " + content.strip())
					else:
						curr.append(subpart_name + ":" + content.strip())
						curr_subpart_names.append(subpart_name)
					subpart_name = ""
					content = ""
				elif l[-1] == "{":
					in_subpart = True
					subpart_name = l[:-4]
				elif in_subpart:
					content += l + " "
				elif l[:7] == "created":
					curr.append("created:" + l.split("=",1)[1].lstrip())
				elif l[:8] == "color = ":
					if "color" in curr_subpart_names:
						tmp = list(filter(lambda x: x[:len(subpart_name)] == subpart_name, curr))[0]
						curr.remove(tmp)
						curr.append(tmp + " " + l[8:].strip())
					else:
						curr.append("color:" + l[8:])
						curr_subpart_names.append("color")
				elif "=" in l:
					curr.append(l.split("=",1)[1].lstrip())
				else:
					continue
	except OSError:
		print("Could not open file: " + filename)
	print("Enter file name; enter empty string to finish")
	filename = input().strip()
if has_tribes:
	labels += ";tribe"
fw = open('cultures.csv', 'w')
fw.write(labels + '\n')
fw.writelines(cultures)
fw.close()
	
