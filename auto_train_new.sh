l=`python script/auto_calculate.py conf.json FEATURE_ENABLE_EXPLAIN`
array=$l
for i in ${array[*]}
do
	echo $i
	python script/auto_calculate.py conf.json $i 
	echo $i 'feature calculated!'
done
python script/auto_calculate.py conf.json FUSE
echo 'feature fused!'
python script/auto_calculate.py conf.json LABEL
echo 'data has been labeled!'
sh train.sh
echo 'training process finished'
python script/auto_calculate.py conf.json ANALYZE
