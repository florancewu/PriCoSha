# PriCoSha

PriCoSha is a platform for users to connect with their family and friends. It allows users to share content, tag their friends, and post comments. Users can create specified groups to share content privately. Posts can be managed through deletion. Groups can be deleted, but any deletions are permanent.

Login - A user with an existing account can log in to the platform using their email address and password. Once they input their information and submit, the system validates the input by querying the Person table in the database and checks if the password and email matches. If their information is verified, the system will redirect user to the main page that displays their feed.

View shared content items and info about them - Once logged in, the user has access to content items that they posted, items that are public, and content posted in groups that they are in. The system queries the tables "ContentItem", "Tag", and "Share" and sees if the email matches the rows in the table.

Manage Tags - A user that is tagged in a post has to give permission in order for the tag to be posted. They can go to the Tags page to accept or decline a tag. 

Post Content Item - Users are allowed to post content. When posting, they can choose to make the post public or private. If the post is private, they can mark it private and choose what group they want to post it in. The system inserts the data into ContentItem. 

Tag - A user can tag themselves or another user in a post. If a user tags themselves, they still have to accept or decline the tag. If the user is someone else, the tag is pending until the user accepts. The system matches the Tag Item ID with the Item ID in ContentItem to ensure that the content exists. It is assumed that the tagger has access to the post that they are tagging someone else in. 

Add Friend- A user can add another existing user as their friend if a group is created. The system first checks if the other user exists in the Person Table and then inserts their information from the Add Friend form into the table Member. 



View Public Content-
A user is allowed to view public content. Posts that are posted by users that are not posted to a group are considered public content and can be seen by any users. The system queries the table ContentItem and displays posts that have statuses set to 1. 
Optional Features:

Register - People who want to use the platform but do not have an existing account are allowed to register for an account. Through the "register" button, it will redirect the user to another page that displays a form for them to input their first name, last name, email address, and password. Once the form is submitted, the system wil insert their information into the Person table in the database and allow the user to login.

Add Comments- Users can comment on posts that they made or are tagged in. Those who do not have permisison to view the content are not allowed to add comments to the posts. Once a comment is posted, it can not be removed unless the whole post is deleted. Comments only include text. When a comment is added to a post, the query inserts a row into the Comment table the text, item ID number, and the email of the user who posted the comment.

Defriend- When the user wants to delete a friend, they can input their friend's information into the form(friend's email, friend group name, and user's email). Inputing the user's own email is to confirm their identity. The platform queries for where the user is stored in the database by using their email and friend group name and removes the correlating row from the table Member.
