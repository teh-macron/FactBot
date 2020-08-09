# FactBot
#### A discord bot for maintaining lists of facts

## Setup
This has only been run/tested on CentOS 7, running python 3.6. What you need:
* System running CentOS 7
* Python 3.6 installed
* Access to the internet
* A text file called `token.txt` with your bot's token in it
* All three of the files in this repo (`bot.py`, `build_env.sh`, and `requirements.txt`)

Set the `build_env.sh` script to be executable (`chmod +x build_env.sh`), and run it with all files in the same directory (where you want your venv to be located). This will make a python virtual environment called `FactBot` with all the packages needed to run this bot, and move the files in to the proper place.

## Using the bot
Once you've got the bot running and connected to your Discord Server, here's the commands (as of right now):
##### Category Commands
* `?addcategory` - Adds a fact category. Use `?addcategory "<name>" <id> "<tag>" "<description>"` to add a category
  * The `<name>` should be wrapped in quotes, and is the proper name for the category (i.e. "ChrisWorld Facts")
  * The `<id>` is the short identifier for the category (i.e. `cwf`)
  * The `<tag>` should be wrapped in quotes, and is the leader line you want used for each fact (i.e. "ChrisWorld Fact")
  * The `<description>` should be wrapped in quotes, and is the description for the category (i.e. "Facts about ChrisWorld, a terrible place for anyone but a Chris")
* `?deletecategory` - Deletes a fact category. Use `?deletecategory <category>` to delete a specific fact category.
* `?listcategory` - Lists available Categories. Use `?listcategory` to get a list of category IDs and their descriptions.

###### Fact Commands
* `?addfact` - Adds a fact. Use `?addfact <category> "<fact>"` to add a fact to a category. Wrap the fact in quotes.
* `?deletefact` - Deletes a fact. Use `?deletefact <category> <id#>` to delete a specific fact from the designated category. `<id#>` should be the number of the fact to delete.
* `?fact` - Displays a specific fact. Use `?fact <category> <id#>` to call up a specific fact.
* `?random` - Displays a random fact from a specified category. Use `?random <category>` to print a random fact from the designated category.

###### Misc Commands
* `?help` - Displays the help dialog, with commands and short references for how they work.
* `?help <command>` - Displays more specific details about running a particular command
