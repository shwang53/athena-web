/**
 * GET /
 * index page.
 */



exports.getTestbed = (req, res) => {
   const unknownUser = !(req.user);

   res.render('testbed', {
     title: 'testbed',
     unknownUser,
   });
 };