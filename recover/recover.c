#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    //checks whether only one value was entered
    if (argc != 2)
    {
        printf("Unable to open. Write valid file name\n");
        return 1;
    }

    //Opens the file
    FILE *input = fopen(argv[1], "r");

    //checks whether the file can be opened
    if (input == NULL)
    {
        printf("Unable to open. Insert a valid file\n");
        return 1;
    }

    // initialize buufer, image counter and output file pointer
    unsigned char buffer[512];
    int counter = 0;
    FILE *output = NULL;

    //allocate memory for filename
    char *name = malloc(8 * sizeof(char));

    //reads the input file in sections of blocks
    while (fread(buffer, sizeof(char), 512, input))
    {
        //checks whether it is an opening of a jpg file
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //checks if the output file is open and closes it
            if (output != NULL)
            {
                fclose(output);
            }

            //creates a new output file and names it according to the counter
            sprintf(name, "%03i.jpg", counter);
            output = fopen(name, "w");
            counter++;
        }
        //writes to the output file
        if (output != NULL)
        {
            fwrite(buffer, sizeof(char), 512, output);
        }
    }

    //checks if the output file is open and closes it
    if (output != NULL)
    {
        fclose(output);
    }

    fclose(input);
    free(name);
    return 0;
}