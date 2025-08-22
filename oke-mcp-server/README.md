**Start conductor server**
cd /Users/vivesisi/demo/microtx-conductor-oss/server/build/libs;java -jar -DCONDUCTOR_SECURITY_ENABLED=false -DCONDUCTOR_CONFIG_FILE=./application.properties conductor-server-3.21.14-oracle-microtx-boot.jar

**Start UI**
cd /Users/vivesisi/demo/conductor/conductor-server.old/ui; yarn run start