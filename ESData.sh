ssh -i ssh_key deployer@52.163.206.237
sudo su
ssh -i /var/lib/jenkins/secrets/deployer_ssh_key deployer@80.1.0.9


sudo apt-get install curl
curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
sudo apt-get install nodejs
sudo npm install elasticdump -g

elasticdump --input=http://70.0.0.7:9200/compositesearch --output=compositeDownload.json --type=data
sudo scp -i /var/lib/jenkins/secrets/deployer_ssh_key deployer@70.0.0.7:/home/deployer/compositeDownload.json .


