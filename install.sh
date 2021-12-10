function install_packages(){
	error_pyinstaller=$(pyinstaller 2>&1 1>/dev/null)
	error_bs4=$(python -m bs4 2>&1 1>/dev/null)


	if echo "$error_pyinstaller" | grep -q "command not found" || echo "$error_bs4" | grep -qP "No module named bs4$"
	then
		pip install -r requirements.txt

		if [[ $? != 0 ]]
		then 
			echo "Program Encountered an Error with the installation Please check Network"
			exit -2
		fi
	fi


}

function append_path(){
	if ! echo $PATH | grep -q ":$HOME/.local/bin"
	then
		read -p "Allow ~/.local/bin to be appened to environment path for this user to allow pysearch to be run from anywhere (y/n):" choice

		option = $(echo ${choice:0:1} | tr [:upper:] [:lower:])
		
		if [[ $option == "y" ]]
		then
			echo 'export PATH="$PATH":~/.local/bin' >> ~/.bashrc
			source ~/.bashrc
		fi
	fi

}

function install(){
	install_packages
	
	if [[ -e ~/.local/bin/pysearch ]]
	then
		printf "Program Already Installed.\n\n"
		return 0
	fi

	pyinstaller -F pysearch.py
	mv dist/pysearch ~/.local/bin
	
	append_path

	rm -r dist
	printf "Programmed Installed Successfully\n\n"

	return 0
}

install



