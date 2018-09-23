#l=`ls`
#for i in $l:
#do
#	echo $i
#	newfile=`echo $i | sed 's/test\.//g'`
#	echo $newfile
#	mv $i $newfile
#done

l=`ls label_train_folder`
for i in $l
do
	echo $i
	python remov.py < label_train_folder/$i > $1
	mv $1 $label_train_folder/i
done
