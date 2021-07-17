
prepare-docker-build:
	mkdir -p docker/tmp/src
	rm -r -f src/__pycache__
	cp -p src/* docker/tmp/src

	curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=11X-STlWBqvdp1k_Q2VMs31XRJ0PoQOrf" > /dev/null
	curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=`awk '/download/ {print $NF}' ./cookie`&id=11X-STlWBqvdp1k_Q2VMs31XRJ0PoQOrf" -o docker/tmp/flairBBP_backward-pt.pt 


	curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=1UXri84BUH3p_DDoj71GEls6m8qM5v4Pw" > /dev/null
	curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=`awk '/download/ {print $NF}' ./cookie`&id=1UXri84BUH3p_DDoj71GEls6m8qM5v4Pw" -o docker/tmp/flairBBP_forward-pt.pt 

	rm ./cookie

	curl -L -o data/preprocess/nomes.csv.gz https://data.brasil.io/dataset/genero-nomes/nomes.csv.gz
	gzip -d data/preprocess/nomes.csv.gz

build: prepare-docker-build
	docker-compose -f docker/trainer.yml build
	rm -f -r docker/tmp

compose:
	docker-compose -f docker/trainer.yml -f docker/trainer-dev.yml up