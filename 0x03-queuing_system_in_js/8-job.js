function createPushNotificationsJobs(jobs, queue) {
  if (!Array.isArray(jobs)) {
    throw Error('jobs is not an array');
  }
  jobs.forEach(jobData => {
    const job = queue.create('push_notification_code_3', jobData);

    job.on('complete', () => console.log(`Notification job ${job.id} completed`));

    job.on('failed', () => console.log(`Notification job ${job.id} failed: ${error}`));

    job.on('progress', (progress, data) => {
      console.log(`Notification job ${job.id} ${progress}% complete`);
    });

    job.save((err) => {
      if(!err) {
        console.log(`Notification job created: ${job.id}`);
      }
    });
  });
}

export default createPushNotificationsJobs;
