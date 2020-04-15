#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            BYTE rgbtGrey = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            image[i][j].rgbtBlue = rgbtGrey;
            image[i][j].rgbtGreen = rgbtGrey;
            image[i][j].rgbtRed = rgbtGrey;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            
            int sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
            int sepiaGreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
            int sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);
            
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }
            
            image[i][j].rgbtBlue = sepiaBlue;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtRed = sepiaRed;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int a = 0, b = width - 1; a < width / 2; a++, b--)
        {
            RGBTRIPLE tmp = image[i][a];
            image[i][a] = image[i][b];
            image[i][b] = tmp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE tmp[height][width];
    
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int blue = 0;
            int green = 0;
            int red = 0;
            int total = 0;
            
            blue += image[i][j].rgbtBlue;
            green += image[i][j].rgbtGreen;
            red += image[i][j].rgbtRed;
            total++;
            
            if ((i - 1 >= 0) && (j - 1 >= 0)) // for upper left pixel
            {
                blue += image[i - 1][j - 1].rgbtBlue;
                green += image[i - 1][j - 1].rgbtGreen;
                red += image[i - 1][j - 1].rgbtRed;
                total++;
            }  

            if (i - 1 >= 0) // for upper pixel
            {
                blue += image[i - 1][j].rgbtBlue;
                green += image[i - 1][j].rgbtGreen;
                red += image[i - 1][j].rgbtRed;
                total++;
            }
            
            if ((i - 1 >= 0) && (j + 1 < width)) // for upper right pixel
            {
                blue += image[i - 1][j + 1].rgbtBlue;
                green += image[i - 1][j + 1].rgbtGreen;
                red += image[i - 1][j + 1].rgbtRed;
                total++;
            }            
            
            if (j + 1 < width) // for pixel to the right
            {
                blue += image[i][j + 1].rgbtBlue;
                green += image[i][j + 1].rgbtGreen;
                red += image[i][j + 1].rgbtRed;
                total++;
            }
            
            if ((i + 1 < height) && (j + 1 < width)) // for lower right pixel
            {
                blue += image[i + 1][j + 1].rgbtBlue;
                green += image[i + 1][j + 1].rgbtGreen;
                red += image[i + 1][j + 1].rgbtRed;
                total++;
            }  
            
            if (i + 1 < height) // for lower pixel
            {
                blue += image[i + 1][j].rgbtBlue;
                green += image[i + 1][j].rgbtGreen;
                red += image[i + 1][j].rgbtRed;
                total++;
            } 
            
            if ((i + 1 < height) && (j - 1 >= 0)) // for lower left pixel
            {
                blue += image[i + 1][j - 1].rgbtBlue;
                green += image[i + 1][j - 1].rgbtGreen;
                red += image[i + 1][j - 1].rgbtRed;
                total++;
            }  

            if (j - 1 >= 0) // for left pixel
            {
                blue += image[i][j - 1].rgbtBlue;
                green += image[i][j - 1].rgbtGreen;
                red += image[i][j - 1].rgbtRed;
                total++;
            }
            
            tmp[i][j].rgbtBlue = round(blue / (total * 1.0));
            tmp[i][j].rgbtGreen = round(green / (total * 1.0));
            tmp[i][j].rgbtRed = round(red / (total * 1.0));
        }
    }
    
    for (int i = 0; i < width; i++)
    {
        for (int j = 0; j < height; j++)
        {
            image[j][i].rgbtRed = tmp[j][i].rgbtRed;
            image[j][i].rgbtGreen = tmp[j][i].rgbtGreen;
            image[j][i].rgbtBlue = tmp[j][i].rgbtBlue;
        }
    }
    
    return;
}