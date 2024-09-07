import mongoose from "mongoose";

// Define the Tweet schema
const tweetSchema = new mongoose.Schema({
  user: String,
  createdAt: {
    type : Date,
    default : Date.now
}
    ,
  category: String,
  tweet: String,
});

// Create a Mongoose model
const Tweet = mongoose.model('Tweet', tweetSchema);

export default Tweet