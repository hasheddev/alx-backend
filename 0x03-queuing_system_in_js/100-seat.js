import { createClient } from "redis";

import { createQueue } from 'kue';

import express from 'express';

import { promisify } from 'util';

const client = createClient();

client.on('connect', () => console.log('Redis client connected to the server'));

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

const getAsync = promisify(client.get).bind(client);

function reserveSeat(number) {
  client.set('available_seats', number);  
}

let reservationEnabled = true

async function getCurrentAvailableSeats() {
  const seatCount =  await getAsync('available_seats');
  return seatCount;
}

const queue = createQueue();

const app = express();

app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  return res.json({ numberOfAvailableSeats });
});

app.get('/reserve_seat', (req, res) => {
  if (reservationEnabled == false) {
    return res.json({ "status": "Reservation are blocked" });
  }
  const job = queue.create('reserve_seat', { reservedSeat: 1 }).save(error => {
    if (!error) {
      res.json({ "status": "Reservation in process" });
      console.log(`Seat reservation job created: ${job.id}`);
    } else {
      return res.json({ "status": "Reservation failed" });
    }
  });
  job.on('complete', () => console.log(`Seat reservation job ${job.id} completed`));
  
  job.on('failed', (error) => console.log(`Seat reservation job ${job.id} failed: ${error}`));

});

app.get('/process', (req, res) => {
  res.json({ "status": "Queue processing" });
  queue.process('reserve_seat', async (job, done) => {
    const seat = await getCurrentAvailableSeats();
    const seatCount = parseInt(seat);
    if (seatCount === 0) {
      reservationEnabled = false;
      done(Error('Not enough seats available'));
    } else {
      reserveSeat(seatCount - 1);
      done();
    }
  });
});

app.listen(1245);

reserveSeat(50);
