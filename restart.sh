cd /CommonAssessmentTool
sudo git pull
sudo docker rm -f cs5500 
sudo docker build -t cs5500:latest .
sudo docker run -d -p 8000:8000 --name cs5500 cs5500:latest