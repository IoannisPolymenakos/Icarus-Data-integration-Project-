-- Icarus Tables


  CREATE TABLE "SYSTEM"."AIRPORTS" 
   ("IATA" VARCHAR2(10 BYTE), 
	"ICAO" VARCHAR2(10 BYTE), 
	"NAME" VARCHAR2(255 BYTE), 
	"LOCATION" VARCHAR2(255 BYTE), 
	"TIME" VARCHAR2(50 BYTE), 
	"ID" VARCHAR2(255 BYTE), 
	"SKYID" VARCHAR2(10 BYTE)
   ) 
   
   
  
     CREATE TABLE "SYSTEM"."FLIGHTS_FROM_GREEK_AIRPORTS" 
   ("ID" VARCHAR2(50 BYTE), 
	"LOCATIONNAME" VARCHAR2(100 BYTE), 
	"SKYCODE" VARCHAR2(10 BYTE), 
	"CHEAPESTPRICE" NUMBER, 
	"CHEAPESTDIRECT" VARCHAR2(5 BYTE), 
	"DIRECTPRICE" NUMBER, 
	"FROMID" VARCHAR2(100 BYTE), 
	"DEPARTDATE" DATE, 
	"AIRLINE" VARCHAR2(2000 BYTE)
   )



 CREATE TABLE "SYSTEM"."FLIGHT_RADAR_AIRPORT_INFO" 
   ("NAME" VARCHAR2(100 BYTE), 
	"CITY" VARCHAR2(100 BYTE), 
	"COUNTRY" VARCHAR2(100 BYTE), 
	"IATA_CODE" VARCHAR2(10 BYTE), 
	"ICAO_CODE" VARCHAR2(10 BYTE), 
	"LATITUDE" NUMBER(9,6), 
	"LONGITUDE" NUMBER(9,6)
   ) 
   
   
   
   
    CREATE TABLE "SYSTEM"."FLIGHT_RADAR_AIRPORT_STATS" 
   ("STAT_DATE" DATE, 
	"IATA_CODE" VARCHAR2(10 BYTE), 
	"TEMPERATURE" VARCHAR2(20 BYTE), 
	"WIND_DIRECTION" VARCHAR2(50 BYTE), 
	"WIND_SPEED" VARCHAR2(50 BYTE), 
	"SKY_CONDITION" VARCHAR2(50 BYTE), 
	"DELAY_INDEX" NUMBER, 
	"AVERAGE_DELAY" NUMBER, 
	"ON_TIME_FLIGHTS" NUMBER, 
	"DELAYED_FLIGHTS" NUMBER, 
	"CANCELLED_FLIGHTS" NUMBER, 
	"TREND" VARCHAR2(20 BYTE), 
	"TOTAL_FLIGHTS_TODAY" NUMBER, 
	"DELAYED_FLIGHTS_TODAY" NUMBER, 
	"CANCELLED_FLIGHTS_TODAY" NUMBER, 
	"DELAYED_PERCENTAGE" NUMBER, 
	"CANCELLED_PERCENTAGE" NUMBER
   ) 