/**
 * GET /
 * index page.
 */



exports.getPublication = (req, res) => {
   const unknownUser = !(req.user);

   res.render('publication', {
     title: 'Publication',
     unknownUser,
   });
 };

// exports.postPublication = (req, res) => {
//   return res.redirect('/publication')
// };
