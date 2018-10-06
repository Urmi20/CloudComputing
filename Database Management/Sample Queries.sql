USE `InstaKilo`

insert into users 
	( id, profile, name, first_name, last_name, email, pw_salt_hash ) 
values 
	( DEFAULT,  
	(select id from user_profiles where type = "user"),
	"felipec",
	"Felipe",
	"Sander Pereira Clark",
	"felipe.clark@mail.utoronto.ca",
	"grgrgregergdafnjtj" )
    
insert into users 
	( id, profile, name, first_name, last_name, email, pw_salt_hash ) 
values 
	( DEFAULT,  
	(select id from user_profiles where type = "admin"),
    "root",
    "ADMINISTRATOR",
    "ALL POWERFUL",
    "admin@instakilo.com",
	"kloevnjiwdvawghuo" )

insert into photos 
	( id, owner, title, hashtags, file_name ) 
values 
	( DEFAULT, (select id from users where name = "root"),
    "Veil of Elysium",
    "#waterfall, #long exposure, #nature",
    "c:/photos/root/IMG_1498.jpg")
    
insert into transformations
	( id, original, trans_type, file_name )
values  
	( DEFAULT,
    (select id from photos where file_name = "c:/photos/root/IMG_1498.jpg"),
    (select id from transformation_type where description = "Barrel Distortion"),
    "c:/photo/root/IMG_1498_barrel.jpg")