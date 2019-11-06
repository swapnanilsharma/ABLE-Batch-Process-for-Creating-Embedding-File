mkdir -p downloadedModel
cd downloadedModel

mkdir -p useModel
wget 'https://tfhub.dev/google/universal-sentence-encoder-large/3?tf-hub-format=compressed' -O useModel/temp
tar -zxvf useModel/temp -C useModel/
rm -rf useModel/temp

