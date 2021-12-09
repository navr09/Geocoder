# derilinx-case-study

Approach for geocoder:

1) Read the CSV file containing the list of test addresses and convert it into a Pandas dataframe. We also read the
   reference files as well.
Explanation - The data is stored in a table format using pandas, a library which is well known for handling large datasets
             efficiently. Pandas provide a huge feature set to apply on the data you have so that you can customize, edit
             and pivot it according to your own will and desire. This helps to bring the most out of your data.

2) Parse the address to separate the different parts of the data using the delimiter comma.
Explanation - This is done by reversing the address as Counties is the highest break of the address of Ireland.

3) Data Pre-processing
Explanation - We convert the address of the test data and the reference data to all lower case as this would help in the
matching of the address for retrieving the co-ordinates of the address. We also strip words such as "Co." pre-fix which
are sometimes used in addresses to mention the County.

4) Join on Counties and townlands
Explanation - We then left join the test address with the reference tables of Counties and Townlands in order to retrieve
respective co-ordinates of the address.

5) Co-ordinate conversion
Explanation - We have converted the co-ordinates of the address from ITM(EPSG:2157) to WGS84(EPSG:4326) using Pyproj library.
The conversion is at a townlands level if there is a townland, else it is at a county level.

6) Output generated.
Explanation - Output generated is stored as a CSV file with a timestamp which would be useful to view at a later time too!

7) The Front-end screen makes it easy to verify the address shown by the latitude and longitude. And as always, it adds
charm to the code by bringing it to life!




Advantages of the application:

Modularised codebase- Efficient change of functionalities as the skeleton of the code is loosely coupled.
                      Properties file contains all values which could be changed easily without changing the main code

Faster functions used - Use of recursive function over loops makes it convenient to scale as the number of columns
                        created depends on the address level of the input file.
                        Use of functions such as lambda and apply speed up the time constraint when compared to
                        iterrows(),dict() and index.
                   Reference - https://towardsdatascience.com/400x-time-faster-pandas-data-frame-iteration-16fb47871a0a

Logging and exception handling - Making sure that the application doesn't crash given a certain unforeseen case pops up
                                 in the codebase. Also backtracking is convenient, thanks to the logs.

API-Flask - Usage of an API makes it convenient to run multiple requests to the same server. As this is a single application
            and a lightweight one, I have used flask as it is comparatively faster.
            Reference: https://www.guru99.com/flask-vs-django.html#:~:text=Flask%20is%20a%20Python%20web,offers%20a%20Monolithic%20working%20style.&text=Flask%20is%20WSGI%20framework%20while%20Django%20is%20a%20Full%20Stack%20Web%20Framework.

Javascript front-end - This makes it easier to download the results into a csv and also view the map to check the co-ordinates




Disadvantages of the application:

Local host - This application at the moment can only run locally and might also increase run time. Using cloud service like
             AWS or GCP along with storage facilities like S3 would increase the application performance

Time constraint - Use of database SQL vs NoSQL
                  Use to database to navigate between output and input source would be faster than file system
                  We could use NoSQL if we choose to consider a JSON input as the address form isn't fixed across
                  multiple requests. ALthough this would mean that it is prone to violation of ACID properties, this
                  would be a faster and more efficient usage of storage as allocation is dynamic across requests

JSON post input - Use post request to navigate between file input and webpage parameters

Sequential requests handling - Use of Asyncio/tornado-python
