#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    float avg = 0;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //Calculate the average
            avg = (image[i][j].rgbtBlue) + (image[i][j].rgbtGreen) + (image[i][j].rgbtRed);
            avg /= 3.0;
            int gray = round(avg);

            //Compares all values to make everything gray
            (image[i][j].rgbtBlue) = (image[i][j].rgbtGreen) = (image[i][j].rgbtRed) = gray;
        }
    }
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int sepiaRed;
    int sepiaGreen;
    int sepiaBlue;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //calculating the sepia algorithm
            float Red = (.393 * image[i][j].rgbtRed) + (.769 * image[i][j].rgbtGreen) + (.189 * image[i][j].rgbtBlue);
            float Green = (.349 * image[i][j].rgbtRed) + (.686 * image[i][j].rgbtGreen) + (.168 * image[i][j].rgbtBlue);
            float Blue = (.272 * image[i][j].rgbtRed) + (.534 * image[i][j].rgbtGreen) + (.131 * image[i][j].rgbtBlue);

            //Defines a new sepia red
            if (Red > 255)
            {
                sepiaRed = 255;
            }
            else
            {
                sepiaRed = round(Red);
            }

            //Defines a new sepia green
            if (Green > 255)
            {
                sepiaGreen = 255;
            }
            else
            {
                sepiaGreen = round(Green);
            }

            //Defines a new sepia blue
            if (Blue > 255)
            {
                sepiaBlue = 255;
            }
            else
            {
                sepiaBlue = round(Blue);
            }

            //Applies the new values
            image[i][j].rgbtBlue = sepiaBlue;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtRed = sepiaRed;
        }
    }
}
// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int midle = width - 1;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            //swaping the positions of the pixels
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][midle - j];
            image[i][midle - j] = temp;
        }
    }
}
// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //Creates a copy of the images
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float sumRed = 0;
            float sumGreen = 0;
            float sumBlue = 0;
            int count = 0;

            for (int row = i - 1; row <= i + 1; row++)
            {
                for (int col = j - 1; col <= j + 1; col++)
                {
                    if ((row >= 0) && (col >= 0) && (row < height) && (col < width))
                    {
                        //Calculates the average of the envelope of each pixel
                        sumRed += copy[row][col].rgbtRed;
                        sumGreen += copy[row][col].rgbtGreen;
                        sumBlue += copy[row][col].rgbtBlue;
                        count++;
                    }
                }
            }
            //Changes each pixel to the new value
            image[i][j].rgbtRed = round(sumRed / count);
            image[i][j].rgbtGreen = round(sumGreen / count);
            image[i][j].rgbtBlue = round(sumBlue / count);

        }

    }

}
