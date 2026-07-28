HOW TO ADD A DOCUMENT EXAMPLE TO THE PORTAL
===========================================

1. Drop the PDF into this "documents" folder.
   Use a simple filename, no spaces:   welcome-letter-example.pdf

2. Open index.html and find the PROGRAMS list (search for "const PROGRAMS").

3. Find the document you want to attach and fill in its "file" value:

       { t:'Pre-Launch Announcement Letter', file:'documents/welcome-letter-example.pdf',
         purpose: ...

   Leave file:'' and the card shows a neutral "Example being added" chip instead.
   As soon as a filename is present, View and Download buttons appear automatically.

4. Commit and push. The portal updates within about a minute.

Nothing else needs changing - the layout, ordering and styling are automatic.
