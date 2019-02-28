# -*- coding: utf-8 -*-

##############################################################################
#                        2014 E2OpenPlugins                                  #
#                                                                            #
#  This file is open source software; you can redistribute it and/or modify  #
#     it under the terms of the GNU General Public License version 2 as      #
#               published by the Free Software Foundation.                   #
#                                                                            #
##############################################################################
# Simulate the oe-a boxbranding module (Only functions required by OWIF)     #
##############################################################################

# from Components.About import about
from Tools.Directories import fileExists
from time import time
import os
import hashlib

try:
	from Components.About import about
except ImportError:
	pass


def validate_certificate(cert, key):
	buf = decrypt_block(cert[8:], key)
	if buf is None:
		return None
	return buf[36:107] + cert[139:196]


def get_random():
	try:
		xor = lambda a, b: ''.join(chr(ord(c) ^ ord(d)) for c, d in zip(a, b * 100))
		random = os.urandom(8)
		x = str(time())[-8:]
		result = xor(random, x)

		return result
	except:  # noqa: E722
		return None


def bin2long(s):
	return reduce(lambda x, y: (x << 8L) + y, map(ord, s))


def long2bin(l):
	res = ""
	for byte in range(128):
		res += chr((l >> (1024 - (byte + 1) * 8)) & 0xff)
	return res


def rsa_pub1024(src, mod):
	return long2bin(pow(bin2long(src), 65537, bin2long(mod)))


def decrypt_block(src, mod):
	if len(src) != 128 and len(src) != 202:
		return None
	dest = rsa_pub1024(src[:128], mod)
	hash = hashlib.sha1(dest[1:107])
	if len(src) == 202:
		hash.update(src[131:192])
	result = hash.digest()
	if result == dest[107:127]:
		return dest
	return None


def getAllInfo():
	info = {}

	brand = "unknown"
	model = "unknown"
	procmodel = "unknown"
	grabpip =0
	lcd = 0

	if fileExists("/proc/stb/info/hwmodel"):
		brand = "DAGS"
		f = open("/proc/stb/info/hwmodel", 'r')
		procmodel = f.readline().strip()
		f.close()
		if (procmodel.startswith("optimuss") or procmodel.startswith("pingulux")):
			brand = "Edision"
			model = procmodel.replace("optimmuss", "Optimuss ").replace("plus", " Plus").replace(" os", " OS")
		if (procmodel.startswith("tm")):
			brand = "Technomate"
			if procmodel == "tmnanosem2":
				model = procmodel.replace("tmnanosem2", "TM-NANO-SE M2")
		elif (procmodel.startswith("fusion") or procmodel.startswith("purehd") or procmodel.startswith("revo4k") or procmodel.startswith("galaxy4k")):
			brand = "Xsarius"
			if procmodel == "fusionhd":
				model = procmodel.replace("fusionhd", "Fusion HD")
			elif procmodel == "fusionhdse":
				model = procmodel.replace("fusionhdse", "Fusion HD SE")
			elif procmodel == "purehd":
				model = procmodel.replace("purehd", "Pure HD")
			elif procmodel == "purehdse":
					model = procmodel.replace("purehdse", "Pure HD SE")
			elif procmodel == "revo4k":
				model = procmodel.replace("revo4k", "Revo4K")
			elif procmodel == "galaxy4k":
				model = procmodel.replace("galaxy4k", "Galaxy4K")
		elif (procmodel.startswith("lunix")):
			brand = "Qviart"
			if procmodel == "lunix3-4k":
				model = procmodel.replace("lunix3-4k", "Lunix3-4K")
			elif procmodel == "lunix":
				model = procmodel.replace("lunix", "Lunix")
	elif fileExists("/proc/stb/info/azmodel"):
		brand = "AZBox"
		f = open("/proc/stb/info/model", 'r')  # To-Do: Check if "model" is really correct ...
		procmodel = f.readline().strip()
		f.close()
		model = procmodel.lower()
	elif fileExists("/proc/stb/info/gbmodel"):
		brand = "GigaBlue"
		f = open("/proc/stb/info/gbmodel", 'r')
		procmodel = f.readline().strip()
		f.close()
		if procmodel == "GBQUAD PLUS":
			model = procmodel.replace("GBQUAD", "Quad").replace("PLUS", " Plus")
		elif procmodel == "gbquad4k":
			model = procmodel.replace("gbquad4k", "UHD Quad 4K")
		elif procmodel == "gbue4k":
			model = procmodel.replace("gbue4k", "UHD UE 4K")
		elif procmodel == "gbtrio4k":
			model = procmodel.replace("gbtrio4k", "UHD Trio 4K")
	elif fileExists("/proc/stb/info/vumodel") and not fileExists("/proc/stb/info/boxtype"):
		brand = "Vu+"
		f = open("/proc/stb/info/vumodel", 'r')
		procmodel = f.readline().strip()
		f.close()
		model = procmodel.title().replace("olose", "olo SE").replace("olo2se", "olo2 SE").replace("2", "²").replace("4Kse", "4K SE")
	elif fileExists("/proc/boxtype"):
		f = open("/proc/boxtype", 'r')
		procmodel = f.readline().strip().lower()
		f.close()
		if procmodel in ("adb2850", "adb2849", "bska", "bsla", "bxzb", "bzzb"):
			brand = "Advanced Digital Broadcast"
			if procmodel in ("bska", "bxzb"):
				model = "ADB 5800S"
			elif procmodel in ("bsla", "bzzb"):
				model = "ADB 5800SX"
			elif procmodel == "adb2849":
				model = "ADB 2849ST"
			else:
				model = "ADB 2850ST"
		elif procmodel in ("esi88", "uhd88"):
			brand = "Sagemcom"
			if procmodel == "uhd88":
				model = "UHD 88"
			else:
				model = "ESI 88"
	elif fileExists("/proc/stb/info/boxtype"):
		f = open("/proc/stb/info/boxtype", 'r')
		procmodel = f.readline().strip().lower()
		f.close()
		if procmodel.startswith("et"):
			if procmodel == "et7000mini":
				brand = "Galaxy Innovations"
				model = "ET-7000 Mini"
			elif procmodel == "et11000":
				brand = "Galaxy Innovations"
				model = "ET-11000"
			else:
				brand = "Xtrend"
				model = procmodel.upper()
		elif procmodel.startswith("xpeed"):
			brand = "Golden Interstar"
			model = procmodel
		elif procmodel.startswith("xp"):
			brand = "MaxDigital"
			model = procmodel.upper()
		elif procmodel.startswith("ixuss"):
			brand = "Medialink"
			model = procmodel.replace(" ", "")
		elif procmodel == "formuler4turbo":
			brand = "Formuler"
			model = "F4 Turbo"
		elif procmodel.startswith("formuler"):
			brand = "Formuler"
			model = procmodel.replace("formuler", "")
			if model.isdigit():
				model = 'F' + model
		elif procmodel == "mbtwinplus":
			brand = "Miraclebox"
			model = "Premium Twin+"
		elif procmodel == "alphatriplehd":
			brand = "SAB"
			model = "Alpha Triple HD"
		elif procmodel in ("7000s", "mbmicro"):
			procmodel = "mbmicro"
			brand = "Miraclebox"
			model = "Premium Micro"
		elif procmodel in ("7005s", "mbmicrov2"):
			procmodel = "mbmicrov2"
			brand = "Miraclebox"
			model = "Premium Micro v2"
		elif procmodel.startswith("ini"):
			if procmodel.endswith("9000ru"):
				brand = "Sezam"
				model = "Marvel"
			elif procmodel.endswith("5000ru"):
				brand = "Sezam"
				model = "hdx"
			elif procmodel.endswith("1000ru"):
				brand = "Sezam"
				model = "hde"
			elif procmodel.endswith("5000sv"):
				brand = "Miraclebox"
				model = "mbtwin"
			elif procmodel.endswith("1000sv"):
				brand = "Miraclebox"
				model = "Premium Mini"
			elif procmodel.endswith("1000de"):
				brand = "Golden Interstar"
				model = "Xpeed LX"
			elif procmodel.endswith("9000de"):
				brand = "Golden Interstar"
				model = "Xpeed LX3"
			elif procmodel.endswith("1000lx"):
				brand = "Golden Interstar"
				model = "Xpeed LX"
			elif procmodel.endswith("de"):
				brand = "Golden Interstar"
			elif procmodel.endswith("1000am"):
				brand = "Atemio"
				model = "5x00"
			elif procmodel.endswith("8000am"):
				brand = "Atemio"
				model = "Nemesis"
			elif procmodel.endswith("8000am"):
				brand = "Miraclebox"
				model = "Premium Ultra"
			elif procmodel.endswith("3000"):
				brand = "Venton Unibox"
				model = "HD1"					
			else:
				brand = "Venton"
				model = "HDx"
		elif procmodel.startswith("unibox-"):
			brand = "Venton"
			model = "HDe"
		elif procmodel == "hd1100":
			brand = "Mut@nt"
			model = "HD1100"
		elif procmodel == "hd1200":
			brand = "Mut@nt"
			model = "HD1200"
		elif procmodel == "hd1265":
			brand = "Mut@nt"
			model = "HD1265"
		elif procmodel == "hd2400":
			brand = "Mut@nt"
			model = "HD2400"
		elif procmodel == "hd51":
			brand = "Mut@nt"
			model = "HD51"
			grabpip = 1
		elif procmodel == "hd11":
			brand = "Mut@nt"
			model = "HD11"
		elif procmodel == "hd500c":
			brand = "Mut@nt"
			model = "HD500c"
		elif procmodel == "hd530c":
			brand = "Mut@nt"
			model = "HD530c"
		elif procmodel =="hd60":
			brand ="Mut@nt"
			model = "HD60"
		elif procmodel == "arivalink200":
			brand = "Ferguson"
			model = "Ariva @Link 200"
		elif procmodel.startswith("spark"):
			brand = "Fulan"
			if procmodel == "spark7162":
				model = "Spark 7162"
			else:
				model = "Spark"
		elif procmodel == "spycat":
			brand = "Spycat"
			model = "Spycat"
		elif procmodel == "spycatmini":
			brand = "Spycat"
			model = "Spycat Mini"
		elif procmodel == "spycatminiplus":
			brand = "Spycat"
			model = "Spycat Mini+"
		elif procmodel == "spycat4kmini":
			brand = "Spycat"
			model = "spycat 4K Mini"
		elif procmodel in ("k1pro", "k2pro", "k2prov2", "k3pro", "k1plus"):
			brand = "Mecool"
			model = procmodel
		elif procmodel.startswith("kvi"):
			brand = "Khadas"
			model = procmodel
		elif procmodel in ("c300", "c300pro", "c400plus"):
			brand = "Magicsee"
			model = procmodel
		elif procmodel == "vipercombo":
			brand = "Amiko"
			model = "ViperCombo"
		elif procmodel == "vipert2c":
			brand = "Amiko"
			model = "ViperT2C"
		elif procmodel == "vipercombohdd":
			brand = "Amiko"
			model = "ViperComboHDD"
		elif procmodel.startswith("wetek"):
			brand = "WeTeK"
			model = procmodel
		elif procmodel.startswith("os"):
			brand = "Edision"
			if procmodel == "osmini":
				model = "OS Mini"
			elif procmodel == "osminiplus":
				model = "OS Mini+"
			elif procmodel == "osmega":
				model = "OS Mega"
			elif procmodel == "osnino":
				model = "OS Nino"
			elif procmodel == "osninoplus":
				model = "OS Nino+"
			elif procmodel == "osninopro":
				model = "OS Nino Pro"
			else:
				model = procmodel
		elif procmodel == "h3":
			brand = "Zgemma"
			model = "H3 series"
		elif procmodel == "h4":
			brand = "Zgemma"
			model = "H4 series"
		elif procmodel == "h5":
			brand = "Zgemma"
			model = "H5 series"
		elif procmodel == "h6":
			brand = "Zgemma"
			model = "H6 series"
		elif procmodel == "h7":
			brand = "Zgemma"
			model = "H7 series"
			grabpip = 1
		elif procmodel == "h9":
			brand = "Zgemma"
			model = "H9 series"
		elif procmodel == "lc":
			brand = "Zgemma"
			model = "LC"
		elif procmodel == "sh1":
			brand = "Zgemma"
			model = "Star series"
		elif procmodel == "i55":
			brand = "Zgemma"
			model = "i55"
		elif procmodel == "i55plus":
			brand = "Zgemma"
			model = "i55Plus"
		elif procmodel == "vs1500":
			brand = "Vimastec"
			model = "vs1500"
			grabpip = 1
		elif procmodel.startswith("sf"):
			brand = "Octagon"
			model = procmodel
		elif procmodel == "e4hdultra":
			brand = "Axas"
			model = "E4HD"
			lcd = 1
			grabpip = 1
	elif fileExists("/proc/stb/info/model"):
		f = open("/proc/stb/info/model", 'r')
		procmodel = f.readline().strip().lower()
		f.close()
		if procmodel == "tf7700hdpvr":
			brand = "Topfield"
			model = "TF7700 HDPVR"
		elif procmodel == "dsi87":
			brand = "Sagemcom"
			model = "DSI 87"
		elif procmodel.startswith("spark"):
			brand = "Fulan"
			if procmodel == "spark7162":
				model = "Spark 7162"
			else:
				model = "Spark"
		elif (procmodel.startswith("dm") and not procmodel == "dm8000"):
			brand = "Dream Multimedia"
			if procmodel == "dm800":
				model = "DM800 HD PVR"
			elif procmodel == "dm800se":
				model = "DM800 HD se"
			elif procmodel == "dm500hd":
				model = "DM500 HD"
			elif procmodel == "dm7020hd":
				model = "DM7020 HD"
			elif procmodel == "dm820":
				model = "DM820 HD"
			elif procmodel == "dm7080":
				model = "DM7080 HD"
			elif procmodel == "dm520":
				model = "DM520 HD"
			elif procmodel == "dm525":
				model = "DM525 HD"
			elif procmodel == "dm900":
				model = "DM900 UHD"
				grabpip = 1
			elif procmodel == "dm920":
				model = "DM920 UHD"
				grabpip = 1
			else:
				model = procmodel.replace("dm", "DM", 1)
		elif procmodel == "dm8000":
			brand = "Dream Multimedia"
			model = "DM8000"
		else:
			model = procmodel

	if fileExists("/etc/model"):
		f = open("/etc/model", 'r')
		ovmodel = f.readline().strip().lower()
		if ovmodel in ("k1pro", "k2pro", "k2prov2", "k3pro", "k1plus"):
			brand = "Mecool"
			model = ovmodel
			procmodel = ovmodel
		elif ovmodel.startswith("kvi"):
			brand = "Khadas"
			model = ovmodel
			procmodel = ovmodel
		elif ovmodel in ("c300", "c300pro", "c400plus"):
			brand = "Magicsee"
			model = ovmodel
			procmodel = ovmodel

	type = procmodel
	if type in ("et9x00", "et9000", "et9100", "et9200", "et9500"):
		type = "et9x00"
	elif type in ("et6x00", "et6000"):
		type = "et6x00"
	elif type in ("et5x00", "et5000"):
		type = "et5x00"
	elif type in ("et4x00", "et4000"):
		type = "et4x00"
	elif type == "xp1000":
		type = "xp1000"
	elif type in ("bska", "bxzb"):
		type = "nbox_white"
	elif type in ("bsla", "bzzb"):
		type = "nbox"
	elif type == "sagemcom88":
		type = "esi88"
	elif type in ("tf7700hdpvr", "topf"):
		type = "topf"
	elif type == "ini-9000de":
		type = "xpeedlx3"
	elif type == "ini-8000am":
		type = "atemionemesis"
	elif type == "ini-8000am":
		type = "mbultra"		
	elif type == "ini-9000ru":
		type = "sezammarvel"
	elif type == "ini-3000":
		type = "ventonhdx"
	elif type == "ini-1000sv":
		type = "mbmini"			

	info['brand'] = brand
	info['model'] = model
	info['procmodel'] = procmodel
	info['type'] = type

	remote = "dmm1"
	if procmodel in ("solo", "duo", "uno", "solo2", "solose", "zero", "solo4k", "uno4k", "ultimo4k"):
		remote = "vu_normal"
	elif procmodel == "duo2":
		remote = "vu_duo2"
	elif procmodel == "ultimo":
		remote = "vu_ultimo"
	elif procmodel in ("uno4kse", "zero4k", "duo4k"):
		remote = "vu_normal_02"
	elif procmodel == "e3hd":
		remote = "e3hd"
	elif procmodel in ("et9x00", "et9000", "et9100", "et9200", "et9500"):
		remote = "et9x00"
	elif procmodel in ("et5x00", "et5000", "et6x00", "et6000"):
		remote = "et5x00"
	elif procmodel in ("et4x00", "et4000"):
		remote = "et4x00"
	elif procmodel == "et6500":
		remote = "et6500"
	elif procmodel in ("et8x00", "et8000", "et8500", "et8500s", "et10000"):
		remote = "et8000"
	elif procmodel in ("et7x00", "et7000", "et7500"):
		remote = "et7x00"
	elif procmodel in ("et7000mini", "et11000"):
		remote = "et7000mini"
	elif procmodel == "gbquad":
		remote = "gigablue"
	elif procmodel == "gbquadplus":
		remote = "gbquadplus"
	elif procmodel in ("gbquad4k", "gbue4k", "gbtrio4k"):
		remote = "gb7252"
	elif procmodel in ("formuler1", "formuler3", "formuler4", "formuler4turbo"):
		remote = "formuler1"
	elif procmodel in ("azboxme", "azboxminime", "me", "minime"):
		remote = "me"
	elif procmodel in ("optimussos1", "optimussos1plus", "optimussos2", "optimussos2plus"):
		remote = "optimuss"
	elif procmodel in ("premium", "premium+"):
		remote = "premium"
	elif procmodel in ("elite", "ultra"):
		remote = "elite"
	elif procmodel in ("ini-1000", "ini-1000ru"):
		remote = "ini-1000"
	elif procmodel == "ini-1000sv":
		remote = "mbmini"	
	elif procmodel in ("ini-5000sv", "ini-9000de"):
		remote = "xpeedlx3"
	elif procmodel == "ini-9000ru":
		remote = "sezammarvel"		
	elif procmodel == "ini-8000am":
		remote = "atemionemesis"
	elif procmodel == "ini-8000am":
		remote = "mbultra"
	elif procmodel == "ini-3000":
		remote = "ventonhdx"		
	elif procmodel in ("mbtwinplus", "mbmicro", "mbmicrov2"):
		remote = "miraclebox2"
	elif procmodel == "alphatriplehd":
		remote = "alphatriplehd"
	elif procmodel == "ini-3000":
		remote = "ini-3000"
	elif procmodel in ("ini-7012", "ini-7000", "ini-5000", "ini-5000ru"):
		remote = "ini-7000"
	elif procmodel.startswith("spark"):
		remote = "spark"
	elif procmodel == "xp1000":
		remote = "xp1000"
	elif procmodel.startswith("xpeedlx"):
		remote = "xpeedlx"
	elif procmodel in ("adb2850", "adb2849", "bska", "bsla", "bxzb", "bzzb", "esi88", "uhd88", "dsi87", "arivalink200"):
		remote = "nbox"
	elif procmodel in ("hd1100", "hd1200", "hd1265", "hd1400", "hd51", "hd11", "hd500c", "hd530c"):
		remote = "hd1x00"
	elif procmodel == "hd2400":
		remote = "hd2400"
	elif procmodel == "hd60":
		remote = "hd60"
	elif procmodel in ("spycat", "spycatmini", "spycatminiplus", "spycat4kmini"):
		remote = "spycat"
	elif procmodel.startswith("ixuss"):
		remote = procmodel.replace(" ", "")
	elif procmodel == "vg2000":
		remote = "xcombo"
	elif procmodel == "dm8000":
		remote = "dmm1"
	elif procmodel in ("dm7080", "dm7020hd", "dm800sev2", "dm500hdv2", "dm520", "dm525", "dm820", "dm900", "dm920"):
		remote = "dmm2"
	elif procmodel == "wetekhub":
		remote = procmodel
	elif procmodel == "wetekplay2":
		remote = procmodel
	elif procmodel == "wetekplay":
		remote = procmodel
	elif procmodel.startswith("osmio"):
		remote = "edision4"
	elif procmodel.startswith("osm"):
		remote = "osmini"
	elif procmodel.startswith("osninopr"):
		remote = "edision3"
	elif procmodel.startswith("osninopl"):
		remote = "edision2"
	elif procmodel.startswith("osn"):
		remote = "edision1"
	elif procmodel == "fusionhd":
		remote = procmodel
	elif procmodel == "fusionhdse":
		remote = procmodel
	elif procmodel in ("purehd", "purehdse"):
		remote = "purehd"
	elif procmodel in ("revo4k", "galaxy4k"):
		remote = procmodel
	elif procmodel in ("lunix3-4k", "lunix"):
		remote = "qviart"
	elif procmodel in ("sh1", "lc"):
		remote = "sh1"
	elif procmodel in ("h3", "h4", "h5", "h6", "h7", "h9", "i55plus"):
		remote = "h3"
	elif procmodel == "i55":
		remote = "i55"
	elif procmodel in ("vipercombo", "vipert2c"):
		remote = "amiko"
	elif procmodel == "vipercombohdd":
		remote = "amiko1"
	elif procmodel == "alien5":
		remote = "alien5"
	elif procmodel in ("k1pro", "k2pro", "k2prov2", "k1plus", "kvim2", "c300", "c300pro", "c400plus"):
		remote = "k1pro"
	elif procmodel == "k3pro":
		remote = "k3pro"
	elif procmodel.startswith("sf"):
		remote = "octagon"
	elif procmodel in ("vs1100", "vs1500"):
		remote = "vs1x00"
	elif procmodel in ("e4hd"):
		remote = "e4hd"
	elif procmodel in ("tmnanosem2", "tmnanosem2plus"):
		remote = "tmnanosem2"

	info['remote'] = remote

	kernel = about.getKernelVersionString()[0]

	distro = "openpli"
	imagever = "unknown"
	imagebuild = ""
	driverdate = "unknown"

	oever = "PLi-OE"

	if fileExists("/etc/model"):
		distro = "openvision"
		oever = "PLi-OE"
	else:
		# OE 2.2 uses apt, not opkg
		if not fileExists("/etc/opkg/all-feed.conf"):
			oever = "OE 2.2"
		else:
			try:
				f = open("/etc/opkg/all-feed.conf", 'r')
				oeline = f.readline().strip().lower()
				f.close()
				distro = oeline.split( )[1].replace("-all", "")
			except:  # nosec  # noqa: E722
				pass

		if distro in ("openpli", "satdreamgr", "openvision", "openrsi"):
			oever = "PLi-OE"
			try:
				imagelist = open("/etc/issue").readlines()[-2].split()[1].split('.')
				imagever = imagelist.pop(0)
				if imagelist:
					imagebuild = "".join(imagelist)
				else:
					# deal with major release versions only
					if imagever.isnumeric():
						imagebuild = "0"
			except:  # nosec  # noqa: E722
				# just in case
				pass
		else:
			try:
				imagever = about.getImageVersionString()
			except:  # nosec  # noqa: E722
				pass

	# reporting the installed dvb-module version is as close as we get without too much hassle
	driverdate = 'unknown'
	try:
		driverdate = os.popen('/usr/bin/opkg -V0 list_installed *dvb-modules*').readline().split( )[2]  # nosec
	except:  # noqa: E722
		try:
			driverdate = os.popen('/usr/bin/opkg -V0 list_installed *dvb-proxy*').readline().split( )[2]  # nosec
		except:  # noqa: E722
			try:
				driverdate = os.popen('/usr/bin/opkg -V0 list_installed *kernel-core-default-gos*').readline().split( )[2]  # nosec
			except:  # nosec # noqa: E722
				pass

	info['oever'] = oever
	info['distro'] = distro
	info['imagever'] = imagever
	info['imagebuild'] = imagebuild
	info['driverdate'] = driverdate
	info['lcd'] = distro in ("openpli", "satdreamgr", "openvision", "openrsi") and lcd or 0
	info['grabpip'] = distro in ("openpli", "satdreamgr", "openvision", "openrsi") and grabpip or 0
	return info


STATIC_INFO_DIC = getAllInfo()


def getMachineBuild():
	return STATIC_INFO_DIC['procmodel']


def getMachineBrand():
	return STATIC_INFO_DIC['brand']


def getMachineName():
	return STATIC_INFO_DIC['model']


def getMachineProcModel():
	return STATIC_INFO_DIC['procmodel']


def getBoxType():
	return STATIC_INFO_DIC['type']


def getOEVersion():
	return STATIC_INFO_DIC['oever']


def getDriverDate():
	return STATIC_INFO_DIC['driverdate']


def getImageVersion():
	return STATIC_INFO_DIC['imagever']


def getImageBuild():
	return STATIC_INFO_DIC['imagebuild']


def getImageDistro():
	return STATIC_INFO_DIC['distro']

def getLcd():
	return STATIC_INFO_DIC['lcd']

def getGrabPip():
	return STATIC_INFO_DIC['grabpip']

class rc_model:
	def getRcFolder(self):
		return STATIC_INFO_DIC['remote']
