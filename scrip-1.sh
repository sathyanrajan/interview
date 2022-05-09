#!/bin/bash
PROPERTY_FILE=release.properties
if [ ! -f "$PROPERTY_FILE" ]; then
    echo "ERROR: $PROPERTY_FILE does not exist"
    exit 1;
fi


BUILD_LOCATION=$(grep release.build.location $PROPERTY_FILE | cut -f2 -d=)
CLIENT=$(grep client.name $PROPERTY_FILE | cut -f2 -d=)
RELEASE_ARTIFACT_NAME=$(grep release.package.zip.name $PROPERTY_FILE | cut -f2 -d=)
SFTP_DEST_LOCATION=$(grep sftp.destination.fullpath $PROPERTY_FILE | cut -f2 -d=)
SSH_KEY=$(grep ssh.key.fullpath $PROPERTY_FILE | cut -f2 -d=)

if [ -d "$BUILD_LOCATION/$CLIENT" ]
then
    echo "ERROR: $BUILD_LOCATION/$CLIENT  directory already exists, please delete the directory and rerun if the intent is to regenerate artifacts for client"
    exit 1;
fi



if [ -d "./rtemp" ]
then
    rm -rf rtemp
fi

mkdir rtemp
cd rtemp
cp $BUILD_LOCATION/tables_sql.zip .

zip -d tables_sql.zip sql/rollback.sql
cp $BUILD_LOCATION/app_jboss.ear .
cp -R $BUILD_LOCATION/xsd .

zip $RELEASE_ARTIFACT_NAME *
md5sum $RELEASE_ARTIFACT_NAME > $RELEASE_ARTIFACT_NAME-md5sum.txt


mkdir $BUILD_LOCATION/$CLIENT
chmod 755 $BUILD_LOCATION/$CLIENT
cp $RELEASE_ARTIFACT_NAME $BUILD_LOCATION/$CLIENT
cp $RELEASE_ARTIFACT_NAME-md5sum.txt $BUILD_LOCATION/$CLIENT

if [ $CLIENT != 'NON_SFTP_CLIENT' ]; then 
 scp -i $SSH_KEY $RELEASE_ARTIFACT_NAME-md5sum.txt $SFTP_DEST_LOCATION
 scp -i $SSH_KEY $RELEASE_ARTIFACT_NAME  $SFTP_DEST_LOCATION
else
 echo 'WARNING!!! For NON_SFTP_CLIENT the artifacts need to be copied to a different location'
fi