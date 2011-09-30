// Author : Wiesław Herr (herself@makhleb.net)
// Check the included LICENSE file for licensing information
// 
// Checks if the current directory is a mercurial repository
// Works well (and speeds up considerably) with the "hg status" plugin
// ---------------

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>

//returns 1 if we are not in a mercurial repo, 0 otherwise
int main(int argc, const char *argv[])
{
	int ret;
	char* dir_name = NULL;
	struct stat info;

	for(;;){
		//get directory name
		dir_name = getwd(NULL);
		if(dir_name == NULL){
			perror("getwd");
			return -1;
		}

		//root ends the execution
		if(strcmp(dir_name, "/") == 0){
			return 1;
		}

		//memory leaks -- too bad, I don't care
		asprintf(&dir_name, "%s/.hg", dir_name);

		//check if we have .hg in current directory
		ret = stat(dir_name, &info);
		if(ret == 0){
			if(S_ISDIR(info.st_mode)){
				return 0;
			}
		}

		//must... dive... deeper
		ret =	chdir("..");
		if(ret < 0){
			perror("chdir");
			return -1;
		}
	}
	return 1;
}
