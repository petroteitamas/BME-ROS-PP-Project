[//]: # (Image References)
[image1]: ./assets/bme_logo.jpg "BME"
[image2]: ./assets/play_youtube.png "Play on YouTube"
[image3]: ./assets/robot_DH.png "Robot D-H parameters"
[image4]: ./assets/tf_tree.png "TF tree"
[image5]: ./assets/joint_linear_motion.png "Joint vs Linear interpolation"

[image6]: ./assets/Image_process_RAW.png "The image seen by the camera"
[image7]: ./assets/Image_process_RED.png "Image filtered to RED"
[image8]: ./assets/Image_process_GREEN.png "Image filtered to GREEN"





![alt text][image1]

# Robotrendszerek laboratórium projektfeladat


<font size="3">
      Készítették:<br />
      Kovács Tamás Barnabás<em>@kovszegtom</em><br />
      Petrőtei Tamás József <em>@petroteitamas</em><br />
</font>


# Tartalomjegyzék
1. [Feladat bemutatása](#Feladat-bemutatása)  
2. [Program futtatása](#Program-futtatása)
3. [Megvalósítás lépései](#Megvalósítás-lépései)

      3.1. [Robot felépítése](#Robot-felépítése)

      3.2. [Koordinátarendszer felépítése](#Koordinátarendszer-felépítése)

      3.3. [Inverz kinematika megvalósítása](#Inverz-kinematika-megvalósítása)

      3.4. [Képfeldolgozás megvalósítása](#Képfeldolgozás-megvalósítása)

      3.5. [Robot mozgatás](#Robot-mozgatás)
4. [Összegzés](#Összegzés)
5. [Továbbfejlesztési lehetőségek](#Továbbfejlesztési-lehetőségek)


# 1. Feladat bemutatása

A tárgy keretein belül egy olyan robotmanipulációt programot készítettünk el, amely képes egy virtuális kamera segítségével különböző színű kockákat szétválogatni. A program önállóan képes detektálni az elhelyezkedő kockák számát, és azon helyzeteit.



[![alt text][image2]](https://youtu.be/ZBNHiPTMlw4)


# 2. Program futtatása
 
A program indításának első lépése, hogy betöltsük a Gazebo fizikai szimulációs környezetet, majd elindítsuk abban a szimulácitó.

```console
roslaunch bme_ros_pp_project spawn_robot.launch
```
A program egyszerűbb futtatása érdekében létrehoztunk egy bash file-t, így a projekt indítása méggyorsabb tud lenni a következő paranccsal (tab nyomásával a részlegesen beírt parancs kiegészül):

```console
./start.bash
```

Ezt követően két külön modult kell még elindítanunk. Egyrész azt amely az inverz kinematikai számításokat végzi, másrészt azt amely a kameraképet feldolgozza, kiértékeli és kiküldi az előzőleg elindított modulnak.

Tehát indítsuk el a következő két modult
```console
# rosrun bme_ros_pp_project sub_xyzw_ikin_pub_joint.py
./ikin.bash
```

```console
# rosrun bme_ros_pp_project pub_cam.py
./pi.bash
```

A program segítségével a robot önállóan elvégzi a kockák szín szerinti szétválogatását.


# 3. Megvalósítás lépései

## 3.1. Robot felépítése

Az projekt megvalósítása során célunk az volt, hogy a vizuális szemléltetés érdekében egy létező fizikai robotot fogunk a ROS által biztosított szimulációs környezetben megjeleníteni. Mivel az ABB márkájú robotoknak ingyenesen, publikusan hozzáférhető mesh fájljuk van, valamint a dokumentációjuk is számunkra kellő mértékben részletes, továbbá a megvalósítandó feladat 2.5D manipulációval is végrehajtható, így esett a választás az IRB 920-6/0.55 típusú SCARA kinematikájú robotra.

A letöltött STEP modellek koordinátarendszeri nem voltak számunkra megfelelőek, így Inventor segítségével a Denavit-Hartenberg paramétereknek megfelelő koordinátarendszerbe transzformáltuk azokat. Egy online STEP to DAE konverter segítségével átkonvertáltuk a 3D modelljeinket, azonban azzal szembesültünk, hogy Gazibo környezetben a grafika eltűnt. Kisebb utánajárást követően .obj formátumba kiexportált 3D állományokat már meg tudtunk nyitni Blenderben, ahonnan már probléma mentesen ki tudtuk exportálni .dae formátumba.


## 3.2. Koordinátarendszer felépítése
A Khalil-Dombre féle módosított D-H paramétereknek megfelelően a Z tengelyek körül történik az egyes Jointok mozgatása. SCARA felépítésű robot esetében ez a tengely kizárólag függőleges irányú. A felépített koordinátarendszert a következő ábra szemlélteti:

![alt text][image3]
Robot koordinátarendszere

![alt text][image4]
TF tree



## 3.3. Inverz kinematika megvalósítása

A robot descartes koordinátarendszerbeli mozgatásához meg kell oldanunk az inverz kinematikai feladatot. A SCARA felépítésű robot pick and place feladatok megvalósításánál leredukálható 2 DoF-ra, tehát síkban történő mozgatásra, valamint 



Az inverz kinematikai helyes megvalósításáról egy Python kódot is készítettünk, amelyben szemléltetjük mind a csuklótér mind a munkatérbeli lineáris interpolációt.
![alt text][image5]


## 3.4. Képfeldolgozás megvalósítása

Képfeldolgozás segítségével lehetőség van a fizikai könyezetbe elhelyezett kockák helyzeteinek kinyerésére. 
![alt text][image6]

Feldolgozatlan képkocka

![alt text][image7]

Piros színre szűrt kép

![alt text][image8]

Zöld színre szűrt kép

A képfeldolgozás lépései:
 * A kép fogadása (ROS Subscriber)
 * A kép konvertálása (CvBridge)
 * HSV színtérbe konvertálás
 * Színszűrő alkalmazása
 * Zaj eltávolítása nyitás morfológiai művelettel
 * A kép címkézése (objektumok szegmentálása)
 * A kép felcímképett objektumainak helyzeteinek kinyerése.
 * A kamera és a robot koordinátarendszere közötti transzformáció elvégzése.
 * A megtalált objektumhelyzetek listába rendezése, majd kulcs-érték párral ellátott változóba helyezése

 Az így megállapított pozíciók a robot felvételi (Pick pozíciói).


 ## 3.5. Robot mozgatás

A robot a képfeldolgozás során megállapított pontokból egymáshoz képest X irányban, inkrementálisan növelt, előre meghatározott helyzetekbe szállítja a kockákat. A jelen feladatban a két különböző színű kockát két külön sorba helyezi el. 


# 4. Összegzés
A feladat megoldásánál sok, korábbi tárgyból megszerzett ismeretet tudtunk hasznosítani, az elméleti tudásunkat gyakorlati alkalmazásba átültetni.


# 5. Továbbfejlesztési lehetőségek
 1. Orientáció detektálása
 2. Dinamikus kockagenerálás
      Erre egy programot is készítettünk melynek eredményét a következő kép szemlélteti, azonban idő hiányában nem sikerült a programba implementálni.

 3. Több, előre nem definiált szín szerinti szeparáció