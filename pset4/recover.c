#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Check for invalid usage
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // Remember filename
    char *infile = argv[1];

    // Open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }
    
    BYTE buffer[512];
    int counter = 0;
    char outfile[8];
    FILE *outptr = NULL;
                        
    // Read input file, one element of size 512 BYTES at a time while checking that end of file has not been reached
    while (fread(buffer, sizeof(buffer), 1, inptr) == 1)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (counter == 0)
            {
                // Name output file
                sprintf(outfile, "%03i.jpg", counter);
                counter++;
                // Open output file
                outptr = fopen(outfile, "w");
                // Write in output file
                fwrite(buffer, sizeof(buffer), 1, outptr);                    
            }
            
            else
            {
                fclose(outptr);
                    
                // Name output file
                sprintf(outfile, "%03i.jpg", counter);
                counter++;
                // Open output file
                outptr = fopen(outfile, "w");
                // Write in output file
                fwrite(buffer, sizeof(buffer), 1, outptr);
            }
        }    
        
        else if (counter > 0)
        {   
            // Write in already opened output file
            fwrite(buffer, sizeof(buffer), 1, outptr);
        }
    }
    
    fclose(inptr);
    fclose(outptr);
    
    return 0;

}
