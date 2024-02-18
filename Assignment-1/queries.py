queries = ["" for i in range(0, 17)]

#TODO: Finish # 11 12 16s...

### 0. List all the users who have at least 1000 UpVotes.
### Output columns and order: Id, Reputation, CreationDate, DisplayName
### Order by Id ascending
queries[0] = """--sql
select Id, Reputation, CreationDate,  DisplayName
from users
where UpVotes >= 1000
order by Id asc;
"""

### 1. Write a query to find all Posts who satisfy one of the following conditions:
###        - the post title contains 'postgres' and the number of views is at least 50000
###        - the post title contains 'mongodb' and the number of views is at least 25000
### The match should be case insensitive
###
### Output columns: Id, Title, ViewCount
### Order by: Id ascending
queries[1] = """--sql
SELECT Id, Title, ViewCount
FROM Posts
WHERE (LOWER(Title) LIKE '%postgres%' AND ViewCount >= 50000)
   OR (LOWER(Title) LIKE '%mongodb%' AND ViewCount >= 25000)
ORDER BY Id ASC;

"""

### 2. Count the number of the Badges for the user with DisplayName 'JHFB'.
###
### Output columns: Num_Badges
queries[2] = """--sql
SELECT COUNT(*) AS Num_Badges
FROM Badges
WHERE UserId = (
    SELECT Id
    FROM Users
    WHERE DisplayName = 'JHFB'
);
"""

### 3. Find the Users who have received a "Guru" badge, but not a "Curious" badge.
### Only report a user once even if they have received multiple badges with the above names.
###
### Hint: Use Except (set operation).
###
### Output columns: UserId
### Order by: UserId ascending
queries[3] = """--sql
SELECT UserId
FROM Badges
WHERE Name = 'Guru'
EXCEPT
SELECT UserId
FROM Badges
WHERE Name = 'Curious'
ORDER BY UserId ASC;
"""

### 4. "Tags" field in Posts lists out the tags associated with the post in the format "<tag1><tag2>..<tagn>".
### Find the Posts with at least 4 tags, with one of the tags being sql-server-2008 (exact match).
### Hint: use "string_to_array" and "cardinality" functions.
### Output columns: Id, Title, Tags
### Order by Id
queries[4] = """--sql
SELECT Id, Title, Tags
FROM Posts
WHERE
    '<sql-server-2008' = ANY(string_to_array(Tags, '>')) 
    AND cardinality(string_to_array(Tags, '>')) > 4 
ORDER BY Id;
"""

### 5. SQL "with" clause can be used to simplify queries. It essentially allows
### specifying temporary tables to be used during the rest of the query. See Section
### 3.8.6 (6th Edition) for some examples.
###
### Write a query to find the name(s) of the user(s) with the largest number of badges. 
### We have provided a part of the query to build a temporary table.
###
### Output columns: Id, DisplayName, Num_Badges
### Order by Id ascending (there may be more than one answer)

# """
# with temp as (
#         select Users.Id, DisplayName, count(*) as num_badges 
#         from users join badges on (users.id = badges.userid)
#         group by users.id, users.displayname)
# select *
# from temp;
# """

queries[5] = """--sql
WITH temp AS (
    SELECT Users.Id, Users.displayname, COUNT(*) AS num_badges
    FROM Users
    join badges on Users.id = badges.UserId
    GROUP BY Users.id, Users.displayname
)
SELECT id, displayname, num_badges
FROM temp
WHERE num_badges = (SELECT MAX(num_badges) FROM temp)
ORDER BY id ASC;
"""

### 6. "With" clauses can be chained together to simplify complex queries. 
###
### Write a query to associate with each user the number of posts they own as well as the
### number of badges they have received, assuming they have at least one post and
### one badge. We have provided a part of the query to build two temporary tables.
###
### Restrict the output to users with id less than 100.
###
### Output columns: Id, DisplayName, Num_Posts, Num_Badges
### Order by Id ascending
# """
# with temp1 as (
#         select owneruserid, count(*) as num_posts
#         from posts
#         group by owneruserid),
# temp2 as (
#         select userid, count(*) as num_badges
#         from badges
#         group by userid)
# select * 
# from temp1;
# """

queries[6] = """--sql
WITH temp1 AS (
    SELECT OwnerUserId, COUNT(*) AS Num_Posts
    FROM Posts
    GROUP BY OwnerUserId
),
temp2 AS (
    SELECT UserId, COUNT(*) AS Num_Badges
    FROM Badges
    GROUP BY UserId
)
SELECT temp1.OwnerUserId, Users.DisplayName, temp1.Num_Posts, temp2.Num_Badges
FROM temp1
JOIN temp2 ON temp1.OwnerUserId = temp2.UserId
JOIN Users ON temp1.OwnerUserId = Users.Id
WHERE temp1.OwnerUserId < 100
ORDER BY temp1.OwnerUserId ASC;
"""

### 7. A problem with the above query is that it may not include users who have no posts or no badges.
### Use "left outer join" to include all users in the output.
###
### Feel free to modify the "with" clauses to simplify the query if you like.
###
### Output columns: Id, DisplayName, Num_Posts, Num_Badges
### Order by Id ascending
# """
# with temp1 as (
#         select owneruserid, count(*) as num_posts
#         from posts
#         group by owneruserid),
# temp2 as (
#         select userid, count(*) as num_badges
#         from badges
#         group by userid)
# select *
# from temp1;
#--Continue Code From Here
# """
queries[7] = """--sql
with UserPosts as (
    select Users.Id, Users.DisplayName, count(Posts.Id) as Num_Posts
    from Users
    left join Posts on Users.Id = Posts.OwnerUserId
    where Users.Id < 100
    group by Users.Id, Users.DisplayName
),
UserBadges as (
    select Users.Id, count(Badges.Id) as Num_Badges
    from Users
    left join Badges on Users.Id = Badges.UserId
    where Users.Id < 100
    group by Users.Id
)
select UserPosts.Id, UserPosts.DisplayName, UserPosts.Num_Posts, coalesce(UserBadges.Num_Badges, 0) as Num_Badges
from UserPosts
left join UserBadges on UserPosts.Id = UserBadges.Id
order by UserPosts.Id asc;
"""

### 8. List the users who have made a post in 2009.
### Hint: Use "in".
###
### Output Columns: Id, DisplayName
### Order by Id ascending
queries[8] = """--sql
select distinct users.id, users.displayname from users
join posts on users.id = posts.owneruserid where date_part('year', posts.creationdate) = 2009
order by users.id asc;
"""

### 9. Find the users who have made a post in 2009 (between 1/1/2009 and 12/31/2009)
### and have received a badge in 2011 (between 1/1/2011 and 12/31/2011).
### Hint: Use "intersect" and "in".
###
### Output Columns: Id, DisplayName
### Order by Id ascending
queries[9] = """--sql
with posts_2009 as (
    select distinct owneruserid as id
    from posts
    where date_part('year', creationdate) = 2009
),
badges_2011 as (
    select distinct userid as id
    from badges
    where date_part('year', date) = 2011
)
select id, displayname
from users where id in (
    select id from posts_2009
    intersect
    select id from badges_2011
)
order by id asc;
"""

### 10. Write a query to output a list of posts with comments, such that PostType = 'Moderator nomination' 
### and the comment has score of at least 10. So there may be multiple rows with the same post
### in the output.
###
### This query requires joining three tables: Posts, Comments, and PostTypes.
###
### Output: Id (Posts), Title, Text (Comments)
### Order by: Id ascending
queries[10] = """--sql
select posts.id as id, posts.title as title, comments.text as text from posts
join comments on posts.id = comments.postid
join posttypes on posts.posttypeid = posttypes.posttypeid where posttypes.description = 'Moderator nomination' and comments.score >= 10
order by posts.id asc;
"""


### 11. For the users who have received at least 200 badges in total, find the
### number of badges they have received in each year. This can be used, e.g., to 
### create a plot of the number of badges received in each year for the most active users.
###
### There should be an entry for a user for every year in which badges were given out.
###
### We have provided some WITH clauses to help you get started. You may wish to 
### add more (or modify these).
###
### Output columns: Id, DisplayName, Year, Num_Badges
### Order by Id ascending, Year ascending
<<<<<<< HEAD
# with years as (
#         select distinct extract(year from date) as year 
#         from badges),
#      temp1 as (
#         select id, displayname, year
#         from users, years
#         where id in (select userid from badges group by userid having count(*) >= 200)
#      )
# select 0;
queries[11] = """--sql
with eligible_users as (
    select userid from badges
    group by userid having count(*) >= 200
), yearly_badge_counts as (
    select badges.userid, extract(year from badges.date) as year, count(*) as num_badges from badges
    join eligible_users on badges.userid = eligible_users.userid
    group by badges.userid, extract(year from badges.date)
), user_info as (
    select users.id, users.displayname from users
    where users.id in (select userid from eligible_users)
)
select user_info.id, user_info.displayname, yearly_badge_counts.year, yearly_badge_counts.num_badges
from yearly_badge_counts
join user_info on yearly_badge_counts.userid = user_info.id
order by user_info.id asc, yearly_badge_counts.year asc;
=======
###
### NOTE: If the query below fails for you for some reason (it seems to be happening on amd64 image),
### use this query instead -- the output is identical but years are hardcoded:
###
### with temp1 as (
###      select id, displayname, year
###      from users, generate_series(2011, 2022) as year
###      where id in (select userid from badges group by userid having count(*) >= 200))
### select * from temp1;
###
queries[11] = """
with years as (
        select distinct extract(year from date) as year 
        from badges),
     temp1 as (
        select id, displayname, year
        from users, years
        where id in (select userid from badges group by userid having count(*) >= 200)
     )
select 0;
>>>>>>> b931424a998f9a3bb99f9fa687c8ff0bd803b27c
"""
#Not quite right I think

### 12. Find the post(s) that took the longest to answer, i.e., the gap between its creation date
### and the creation date of the first answer to it (in number of days). Ignore the posts with no
### answers. Keep in mind that "AcceptedAnswerId" is the id of the post that was marked
### as the answer to the question -- joining on "parentid" is not the correct way to find the answer.
###
### Hint: Use with to create an appropriate table first.
###
### Output columns: Id, Title, Gap
queries[12] = """--sql
with questionanswergap as (
    select
        posts.id,posts.title,posts.creationdate,answers.creationdate,(answers.creationdate - posts.creationdate) 
    as gap
    from posts
    inner join posts answers on posts.acceptedanswerid = answers.id
    where posts.posttypeid = 1 -- assuming 1 is the posttypeid for questions
)
select id,title,gap
from questionanswergap
order by gap desc
limit 1;
"""


### 13. Write a query to find the posts with at least 7 children, i.e., at
### least 7 other posts have that post as the parent
###
### Output columns: Id, Title
### Order by: Id ascending
queries[13] = """--sql
select p.id, p.title
from posts p
join (
    select parentid, count(*) as child_count
    from posts
    group by parentid
) as child_counts
on p.id = child_counts.parentid
where child_counts.child_count >= 7
order by p.id asc;
"""

### 14. Find posts such that, between the post and its children (i.e., answers
### to that post), there are a total of 100 or more votes
###
### HINT: Use "union all" to create an appropriate temp table using WITH
###
### Output columns: Id, Title
### Order by: Id ascending
queries[14] = """--sql
with post_votes as (
    select p.id, p.title, count(v.id) as votes
    from posts p
    left join votes v on p.id = v.postid 
    where p.parentid is null
    group by p.id
), answer_votes as (
    select p.parentid as id, null as title, count(v.id) as votes
    from posts p
    left join votes v on p.id = v.postid 
    where p.parentid is not null
    group by p.parentid
), combined_votes as (
    select id, max(title) as title, sum(votes) as totalvotes
    from (
        select * from post_votes
        union all
        select * from answer_votes
    ) as subquery
    group by id
    having sum(votes) >= 100
)
select id, title from combined_votes 
order by id asc;
"""

### 15. Let's see if there is a correlation between the length of a post and the score it gets.
### We don't have posts in the database, so we will do this on title instead.
### Write a query to find the average score of posts for each of the following ranges of post title length:
### 0-9 (inclusive), 10-19, ...
###
### We will ignore the posts with no title.
###
### HINT: Use the "floor" function to create the ranges.
###
### Output columns: Range_Start, Range_End, Avg_Score
### Order by: Range ascending
queries[15] = """--sql
select
  floor(length(title) / 10) * 10 as range_start,
  floor(length(title) / 10) * 10 + 9 as range_end,
  avg(score) as avg_score
from posts where title is not null and length(title) > 0
group by floor(length(title) / 10)
order by range_start asc;
"""


### 16. Write a query to generate a table: 
### (VoteTypeDescription, Day_of_Week, Num_Votes)
### where we count the number of votes corresponding to each combination
### of vote type and Day_of_Week (obtained by extract "dow" on CreationDate).
### So Day_of_Week will take values from 0 to 6 (Sunday to Saturday resp.)
###
### Don't worry if a particular combination of Description and Day of Week has 
### no votes -- there should be no row in the output for that combination.
###
### Output column order: VoteTypeDescription, Day_of_Week, Num_Votes
### Order by VoteTypeDescription asc, Day_of_Week asc
queries[16] = """--sql
select votetypes.description as votetypedescription, 
       extract(dow from votes.creationdate) as day_of_week, 
       count(*) as num_votes
from votes
join votetypes on votes.votetypeid = votetypes.votetypeid
group by votetypes.description, extract(dow from votes.creationdate)
order by votetypes.description asc, extract(dow from votes.creationdate) asc;
"""
