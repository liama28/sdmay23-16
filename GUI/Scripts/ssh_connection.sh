USERNAME=sdmay23-16

HOST=10.26.48.7

DEST_DIR=/home/sdmay23-16/Felipe_dir/Attack/spectre-attack/

#Move Attack Code Into Laptop

ssh -l ${USERNAME} ${HOST} "cd ${DEST_DIR};make clean; make;sudo sh collect_Spectre.sh"

#Copy Test Results into local machine
scp sdmay23-16@10.26.52.121:/home/sdmay23-16/Felipe_dir/Attack/spectre-attack/data.txt /Users/felipebautista/Programing_Workspaces/GUI/Tmp/

