#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "cube_move.h"
#define N 3
#define LETTER
#define STEP 30

char cube[6][N*N] = {};
void (*p[6])(char [6][N*N]) = {rotate_U,rotate_R,rotate_F,rotate_D,rotate_L,rotate_B};

void cube_init(void)
{
    int k = 0;
	for(int i = 0; i < 6; i++){
		for(int j = 0; j < 9; j++){
			#ifndef LETTER
			cube[i][j] = k++;
			#else
			cube[i][j] = order[i];
			#endif
		}
	}
}

void printcube(char a[6][N*N]){
	char print_order[] = "4215";
	for(int i = 0; i < N; i++){
		printf("      ");
		for(int j = 0; j < N; j++){
			printf(" %c", a[0][i * N + j]);
		}
		printf("\n");
	}
	for(int i = 0; i < N; i++){
		for(int j = 0; j < 4; j++){
			for(int k = 0; k < N; k++){
				printf(" %c", a[print_order[j] - '0'][i * N + k]);
			}
		}
		printf("\n");
	}
	
	for(int i = 0; i < N; i++){
		printf("      ");
		for(int j = 0; j < N; j++){
			printf(" %c", a[3][i * N + j]);
		}
		printf("\n");
	}
	
}

void rotate_step(void (*rot_face)(char [6][N*N]), int rot_time)
{
	// if (rot_time == 1) rot_face(cube);
	// if (rot_time == 2) rot_face(cube),rot_face(cube);
    // if (rot_time == 3) rot_face(cube),rot_face(cube),rot_face(cube);
	for(int i = 0; i < rot_time; i++){
		rot_face(cube);
	}
}

int main(void)
{
    //srand((unsigned)time(NULL));
    cube_init();
    int j = 0;
    for (int i = 0; i < STEP; i ++)
    {
        srand((unsigned)time(NULL)+ rand());
        j = rand()%6;
        //printf("%s\n",p[j]);
        (p[j])(cube);
    }
    printf("\n\n");
    printcube(cube);
	char output[55];
	for(int i = 0; i < 6; i++){
		for(int j = 0; j < 9; j++){
			output[i*9+j] = cube[i][j];
		}
	}
	output[54] = '\0';
	printf("%s\n", output);
	char cmd[200] = "D:\\vscode_project\\vscode_python\\temp.py ";
	strcat(cmd, output);
	strcat(cmd, " > D:\\vscode_project\\C++\\temp.txt");
	//printf(cmd);
	system(cmd);
	char result[100] = {};
    FILE *fp;
    fp = fopen("temp.txt","r");
    int line_number = 1;
    while( fgets(result, 100, fp) != NULL ) {
        line_number++;
        if (line_number == 17) printf("%s\n", result);
    }
    fclose(fp);
	remove("D:\\vscode_project\\C++\\temp.txt");
    int len = strlen(result);
    char turn_face;
	int turn_time;
    for (int i = 0; i < len; i = i+3)
    {
        turn_face = result[i];
        turn_time = result[i+1] - '0';
		// printf("%c%d\n", turn_face, turn_time);
		if (turn_face == 'F') rotate_step(rotate_F,turn_time);
		if (turn_face == 'U') rotate_step(rotate_U,turn_time);
		if (turn_face == 'R') rotate_step(rotate_R,turn_time);
		if (turn_face == 'B') rotate_step(rotate_B,turn_time);
		if (turn_face == 'D') rotate_step(rotate_D,turn_time);
		if (turn_face == 'L') rotate_step(rotate_L,turn_time);
		// if (turn_face == '(' || turn_time == ')') continue;
    }
	printcube(cube);
    return 0;
}