#!/bin/sh
adminutil=`which django-admin.py`
if [ ! -f "$adminutil" ]
	then
		echo "Error: Cannot find django-admin.py utility, please make sure the script is in your application path. Exiting."
		exit
fi
scriptpath="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $scriptpath
while true; do
    read -p "Please enter the URL path to the new site without the leading or trailing slash (letters, numbers, _ and - are valid characters)? " sitepath
    if [[ $sitepath =~ [^a-zA-Z0-9\_\-]+ ]]
    	then
    		echo "Error: Only letters, numbers, _ (underscore), and - (dash) are allowed in the path."
    	else
    		break
    fi
done
cleanedpath=${sitepath//[^a-zA-Z0-9]/}
projectname="${cleanedpath}_community"
if [ -d "$projectname" ]
	then
		echo "A project with the name $projectname already exists, please choose a different URL path."
		exit
fi
django-admin.py startproject $projectname
#cp production_community_template/production_community/urls.py ${projectname}/${projectname}/
dbpasswd=`openssl rand -base64 32`
dbpasswd=${dbpasswd//[\/\=\+]/}
dbname="miro_${cleanedpath}"
while true; do
    read -p "Require login to view this site? (y/n)? " reqlog
    if [ $reqlog != "y" -a $reqlog != "n" ]
    	then
    		echo "Error: please answer with a 'y' or 'n'"
    elif [ $reqlog == "y" ]
        then
	       authmethod="private"
	       htauth=" "
	       break
    else
	       authmethod="cas"
	       htauth="#"
	       break
    fi
done
sed -e "s/{dbpassword}/$dbpasswd/g" -e "s/{dbname}/$dbname/g" -e "s/{dbuser}/$dbname/g" -e "s/{urlpath}/\/$sitepath/g" -e "s/{authmethod}/$authmethod/g" production_community_template/production_community/settings.py > ${projectname}/${projectname}/settings.py
echo "Enter the MySQL root password at the prompt to create site database and user."
mysql -u root -p -e "CREATE DATABASE ${dbname}; GRANT ALL ON ${dbname}.* TO '${dbname}'@'localhost' IDENTIFIED BY '${dbpasswd}';"
secretkey=`openssl rand -base64 32`
secretkey=${secretkey//[\/\=\+]/}
sed -s "s/{secretkey}/${secretkey}/g"  production_community_template/production_community/secretkey.py > ${projectname}/${projectname}/secretkey.py
python ${projectname}/manage.py syncdb
sed -e "s/{processid}/$cleanedpath/g" -e "s/{baseurl}/\/$sitepath/g" -e "s/{projectname}/$projectname/g" -e "s/{htauth}/$htauth/g" miro.httpconf.template > ${cleanedpath}.conf
mv ${cleanedpath}.conf /etc/httpd/conf.d/mirosites/
chown apache ${projectname}/${projectname}
#add to .gitignore
echo "${projectname}/" >> .gitignore
echo "Site creation complete.  Please run /etc/init.d/httpd configtest to confirm settings before restarting apache."
exit
