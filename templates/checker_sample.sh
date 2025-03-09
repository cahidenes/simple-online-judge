#! /bin/sh

for i in {1..100}; do
	echo $i

	# generate input
	if ! python3 generator.py > input.txt 2> generator_error.txt; then
		exit 1
	fi


	# run code
	echo No output is generated > output.txt
	echo No error is generated > error.txt
	timeout 1s python3 code.py < input.txt > output.txt 2> error.txt
	result=$?
	if [ $result -eq 31744 ]; then
		exit 2
	elif [ $result -ne 0 ]; then
		exit 3
	fi


	# check output
	if ! python3 solution.py < input.txt > expected.txt 2> solution_error.txt; then
		exit 4
	fi

	if ! diff -w output.txt expected.txt > /dev/null; then
		exit 5
	fi
done

exit 0
