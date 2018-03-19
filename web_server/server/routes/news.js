var express = require('express');
var router = express.Router();

var rpc_client = require('../rpc_client/rpc_client');

/* GET news summary list. */
router.get('/userId/:userId/pageNum/:pageNum', function(req, res, next) {
  console.log('Fetching news...');
  user_id = req.params['userId'];
  page_num = req.params['pageNum'];

  rpc_client.getNewsSummariesForUser(user_id, page_num, function(response) {
    res.json(response);
  });
});

/* Log news click. */
router.post('/userId/:userId/newsId/:newsId/newsCategory/:newsCategory', function(req,res, next) {
  console.log('Logging news click...');
  user_id = req.params['userId'];
  news_id = req.params['newsId'];
  user_agent = req.headers['user-agent'];
  news_category = req.params['newsCategory'];

  rpc_client.logNewsClickForUser(user_id, news_id, user_agent, news_category);
  res.status(200);
});

module.exports = router;