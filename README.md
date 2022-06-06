# panopto-download
get videos from panopto saved locally. Uses the embed functionality of panopto to merge the two views

`--url` should be the url of the listing page which should look like `....panopto.com/Panopto/Pages/Sessions/List.aspx?e...` or the video page `....panopto.com/Panopto/Pages/Viewer.aspx.....`

`--auth` is the `.ASPXAUTH` cookie's value after logging in

`--bpath` should be the path to the chrome binary on the system in quotes.

## Example usage

```
python3 hmmm.py --url https://xxxxxxxxx.panopto.com/Panopto/Pages/Sessions/List.aspx\#folderID\=%22xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx%22 --auth AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA --bpath "/usr/bin/google-chrome-stable"
```
