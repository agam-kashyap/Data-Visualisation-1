#include <stdio.h>
#include <string.h>

int main(unsigned argc, char *argv[])
{
	if (argc != 2) {
		fprintf(stderr, "Usage: %s INPUT_FILE\n", argv[0]);
		fprintf(stderr, "      INPUT_FILE: For example, multifield.0030.txt\n");
		return -1;
	}

	// Figure out what input file to open and open it.
	char input_file_name[4096] = "./PlaneSliceData/";
	strcat(input_file_name,argv[1]);
	FILE *infile;
	if ( (infile = fopen(input_file_name, "r")) == NULL) {
		fprintf(stderr,"Could not open %s for reading\n", input_file_name);
		return -2;
	}
	
	char delim[] = ".";
	char *ptr = strtok(argv[1], delim);
	char output_file_name[4096]="";
	for(int i=0; i< 4;i++)
	{
		strcat(output_file_name, ptr);
		strcat(output_file_name, ".");
		ptr = strtok(NULL, delim);
	}
	// Figure out what output file to open and open it.
	strcat(output_file_name, "temp.txt");

	char filepath[4096] = "./PropertyData/";
	strcat(filepath, output_file_name);

	FILE *outfile;
	if ( (outfile = fopen(filepath, "w")) == NULL) {
		fprintf(stderr,"Could not open %s for reading\n", filepath);
		return -3;
	}
	// Scan each input line, grab the density data, and write it to the output
	unsigned long l;
	float	density, temperature, ab_H, ab_HP, ab_He, ab_HeP, ab_HePP, ab_HM, ab_H2, ab_H2P;
	for (l = 0; l < 144800; l++) {
		if (fscanf(infile, "%f %f %f %f %f %f %f %f %f %f",
		   &density, &temperature,
		   &ab_H, &ab_HP, &ab_He, &ab_HeP, &ab_HePP, &ab_HM, &ab_H2, &ab_H2P) != 10) {
			fprintf(stderr,"Could not read line %ld\n", l);
			return -4;
		}
		if (fprintf(outfile, "%0.3E\n", temperature) < 0) {
			fprintf(stderr,"Could not write line %ld\n", l);
			return -5;
		}
	}

	fclose(infile);
	fclose(outfile);

	return 0;
}
