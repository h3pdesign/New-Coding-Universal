#muenchen_info = skills_info_de(city='Muenchen', state='Bayern')
#%%
from bs4 import BeautifulSoup  # For HTML parsing
import urllib.request  # Website connections
import re  # Regular expressions
from time import sleep  # To prevent overwhelming the server between connections
from collections import Counter  # Keep track of our term counts
# Filter out stopwords, such as 'the', 'or', 'and'
from nltk.corpus import stopwords
%matplotlib inline


def text_cleaner_ger(website):
    '''
    This function just cleans up the raw html so that I can look at it.
    Inputs: a URL to investigate
    Outputs: Cleaned text only
    '''
    try:
        site = urllib2.urlopen(website).read()  # Connect to the job posting
    except:
        return   # Need this in case the website isn't there anymore or some other weird connection problem

    soup_obj = BeautifulSoup(site)  # Get the html from the site

    for script in soup_obj(["script", "style"]):
        script.extract()  # Remove these two elements from the BS4 object

    text = soup_obj.get_text()  # Get the text from this

    lines = (line.strip() for line in text.splitlines())  # break into lines

    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

    def chunk_space(chunk):
        chunk_out = chunk + ' '  # Need to fix spacing issue
        return chunk_out

    text = ''.join(chunk_space(chunk) for chunk in chunks if chunk).encode(
        'utf-8')  # Get rid of all blank lines and ends of line

    # Now clean out all of the unicode junk (this line works great!!!)

    try:
        # Need this as some websites aren't formatted
        text = text.decode('unicode_escape').encode('ascii', 'ignore')
    # in a way that this works, can occasionally throw
    except:
        return                                                         # an exception

    # Now get rid of any terms that aren't words (include 3 for d3.js)
    text = re.sub("[^a-zA-Z.+3]", " ", text)
    # Also include + for C++

    text = text.lower().split()  # Go to lower case and split them apart

    stop_words = set(stopwords.words("english"))  # Filter out any stop words
    text = [w for w in text if not w in stop_words]

    # Last, just get the set of these. Ignore counts (we are just looking at whether a term existed
    text = list(set(text))
    # or not on the website)

    return text

sample = text_cleaner_ger(
    'http://www.stepstone.de/stellenangebote--Physiker-Mathematiker-Informatiker-als-Junior-Data-Scientist-m-w-Karlsruhe-und-oder-Hamburg-Blue-Yonder-GmbH--2933351-inline.html?isHJ=false&isHJR=false&ssaPOP=1&ssaPOR=1')

def skills_info_de(city=None, state=None):
    '''
    This function will take a desired city/state and look for all new job postings
    on Indeed.com. It will crawl all of the job postings and keep track of how many
    use a preset list of typical data science skills. The final percentage for each skill
    is then displayed at the end of the collation. 

    Inputs: The location's city and state. These are optional. If no city/state is input, 
    the function will assume a national search (this can take a while!!!).
    Input the city/state as strings, such as skills_info('Chicago', 'IL').
    Use a two letter abbreviation for the state.

    Output: A bar chart showing the most commonly desired skills in the job market for 
    a data scientist. 
    '''

    # searching for data scientist exact fit("data scientist" on Indeed search)
    final_job = 'data+scientist'

    # Make sure the city specified works properly if it has more than one word (such as San Francisco)
    if city is not None:
        final_city = city.split()
        final_city = '+'.join(word for word in final_city)
        final_site_list = ['http://de.indeed.com/Jobs?q=%22', final_job, '%22&l=', final_city,
                           '%2C+', state]  # Join all of our strings together so that indeed will search correctly
    else:
        final_site_list = ['http://de.indeed.com/Jobs?q="', final_job, '"']

    # Merge the html address together into one string
    final_site = ''.join(final_site_list)

    base_url = 'http://de.indeed.com'

    try:
        # Open up the front page of our search first
        html = urllib2.urlopen(final_site).read()
    except:
        # In case the city is invalid
        'That city/state combination did not have any jobs. Exiting . . .'
        return
    soup = BeautifulSoup(html)  # Get the html from the first page

    # Now find out how many jobs there were

    num_jobs_area = soup.find(id='searchCount').string.encode(
        'utf-8')  # Now extract the total number of jobs found
    # The 'searchCount' object has this

    # Extract the total jobs found from the search result
    job_numbers = re.findall('\d+', num_jobs_area)

    if len(job_numbers) > 3:  # Have a total number of jobs greater than 1000
        total_num_jobs = (int(job_numbers[2])*1000) + int(job_numbers[3])
    else:
        total_num_jobs = int(job_numbers[2])

    city_title = city
    if city is None:
        city_title = 'Nationwide'

    # Display how many jobs were found
    print ('There were'), total_num_jobs, ('jobs found,'), city_title

    # This will be how we know the number of times we need to iterate over each new
    num_pages = total_num_jobs/10
    # search result page
    job_descriptions = []  # Store all our descriptions in this list

    for i in xrange(1, num_pages+1):  # Loop through all of our search result pages
        print ('Getting page'), i
        # Assign the multiplier of 10 to view the pages we want
        start_num = str(i*10)
        current_page = ''.join([final_site, '&start=', start_num])
        # Now that we can view the correct 10 job returns, start collecting the text samples from each

        html_page = urllib2.urlopen(current_page).read()  # Get the page

        page_obj = BeautifulSoup(html_page)  # Locate all of the job links
        # The center column on the page where the job postings exist
        job_link_area = page_obj.find(id='resultsCol')

        # Get the URLS for the jobs
        job_URLS = [base_url + link.get('href')
                    for link in job_link_area.find_all('a')]

        # Now get just the job related URLS
        job_URLS = filter(lambda x: 'clk' in x, job_URLS)

        for j in xrange(0, len(job_URLS)):
            final_description = text_cleaner_ger(job_URLS[j])
            if final_description:  # So that we only append when the website was accessed correctly
                job_descriptions.append(final_description)
            # So that we don't be jerks. If you have a very fast internet connection you could hit the server a lot!
            sleep(1)

    print ("Done with collecting the job postings!")
    print ("There were"), len(job_descriptions), ("jobs successfully found.")

    doc_frequency = Counter()  # This will create a full counter of our terms.
    [doc_frequency.update(item) for item in job_descriptions]  # List comp

    # Now we can just look at our final dict list inside doc_frequency

    # Obtain our key terms and store them in a dict. These are the key data science skills we are looking for

    prog_lang_dict = Counter({'R': doc_frequency['r'], 'Python': doc_frequency['python'],
                              'Java': doc_frequency['java'], 'C++': doc_frequency['c++'],
                              'Ruby': doc_frequency['ruby'],
                              'Perl': doc_frequency['perl'], 'Matlab': doc_frequency['matlab'],
                              'JavaScript': doc_frequency['javascript'], 'Scala': doc_frequency['scala']})

    analysis_tool_dict = Counter({'Excel': doc_frequency['excel'],  'Tableau': doc_frequency['tableau'],
                                  'D3.js': doc_frequency['d3.js'], 'SAS': doc_frequency['sas'],
                                  'SPSS': doc_frequency['spss'], 'D3': doc_frequency['d3']})

    hadoop_dict = Counter({'Hadoop': doc_frequency['hadoop'], 'MapReduce': doc_frequency['mapreduce'],
                           'Spark': doc_frequency['spark'], 'Pig': doc_frequency['pig'],
                           'Hive': doc_frequency['hive'], 'Shark': doc_frequency['shark'],
                           'Oozie': doc_frequency['oozie'], 'ZooKeeper': doc_frequency['zookeeper'],
                           'Flume': doc_frequency['flume'], 'Mahout': doc_frequency['mahout']})

    database_dict = Counter({'SQL': doc_frequency['sql'], 'NoSQL': doc_frequency['nosql'],
                             'HBase': doc_frequency['hbase'], 'Cassandra': doc_frequency['cassandra'],
                             'MongoDB': doc_frequency['mongodb']})

    overall_total_skills = prog_lang_dict + analysis_tool_dict + \
        hadoop_dict + database_dict  # Combine our Counter objects

    final_frame = pd.DataFrame(overall_total_skills.items(), columns=[
                               'Term', 'NumPostings'])  # Convert these terms to a
    # dataframe

    # Change the values to reflect a percentage of the postings

    # Gives percentage of job postings
    final_frame.NumPostings = (
        final_frame.NumPostings)*100/len(job_descriptions)
    #  having that term

    # Sort the data for plotting purposes

    final_frame.sort(columns='NumPostings', ascending=False, inplace=True)

    # Get it ready for a bar plot

    final_plot = final_frame.plot(x='Term', kind='bar', legend=None,
                                  title='Percentage of Data Scientist Job Ads with a Key Skill, ' + city_title)

    final_plot.set_ylabel('Percentage Appearing in Job Ads')
    # Have to convert the pandas plot object to a matplotlib object
    fig = final_plot.get_figure()

    return fig, final_frame  # End of the function
