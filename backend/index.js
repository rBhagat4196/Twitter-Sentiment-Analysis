import express from 'express';
import cors from 'cors';
import connectDb from './config/connectDb.js';
import Tweet from './models/tweetsModel.js';


// initializers
const app = express();


// options
// mongodb://127.0.0.1:27017


// middlewares
app.use(express.json());
app.use(
    cors({
      origin: 'http://127.0.0.1:5000',
    })
);

const MONGO_URl = "mongodb://127.0.0.1:27017/tweet"
// Database connection
connectDb(MONGO_URl);

app.post('/tweet',async(req,res)=>{
    const {user,category,tweet} = req.body;
    const newTweet = new Tweet({
        user,
        category,
        tweet
    });
    await newTweet.save();
    res.json("tweets successfully posted")
});

app.get('/tweet/:query/:count',async(req,res)=>{
    const {query,count} = req.params;
    let total = count;
    const data = await Tweet.find(
        {
            $or: [
                { 
                     category: { $regex: new RegExp(query, 'i') } }, // Case-insensitive search for "query" in "title"
                  {  tweet: { $regex: new RegExp(query, 'i') } } // Case-insensitive search for "query" in "address"
                ]
        }
    ).sort({ createdAt: -1 });
    if(data.length < total){
        total = data.length;
    }
    const tweets = data.map((item) => item.tweet)
    res.json(tweets.slice(0,total));
});


app.listen(4000, () => {
    console.log('Server is running on port 4000');
  });