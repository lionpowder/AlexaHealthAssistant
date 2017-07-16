package_folder=".env/lib/python2.7/site-packages"
zip_name="code.zip"

py_files=("main.py" "dbUtil.py")
packages="pymysql"

cp -r $package_folder/$packages $packages
rm $zip_name
zip -r $zip_name ${py_files[*]} $packages
rm -r $packages

aws lambda update-function-code --function-name md_skill_build_profile --zip-file fileb://$zip_name
