To start the bhancha server login as following

    ssh ssh anup@81.4.122.151 -p 4321

Enter password "mundrekovaisi"

    cd bhancha/website

    sudo killall gunicorn

    sudo nohup ./deploy.sh & 
