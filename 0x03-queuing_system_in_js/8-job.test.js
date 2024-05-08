import { createQueue } from 'kue';

import createPushNotificationsJobs from './8-job.js';

import { expect } from 'chai';

const jobs = [
  {
    phoneNumber: '4153518780',
    message: 'This is the code 1234 to verify your account'
  },
  {
    phoneNumber: '4153518781',
    message: 'This is the code 4562 to verify your account'
  },
]

const queue = createQueue();

describe('Test createPushNotificationsJobs function', function () {

  before(function() {
    queue.testMode.enter();
  });

  afterEach(function() {
    queue.testMode.clear();
  });

  after(function() {
    queue.testMode.exit()
  });

  it('tests for error on non array inout', function() {
    expect(() => createPushNotificationsJobs(1, queue)).to.throw(Error);
  });

  it('test for job created', function() {
    createPushNotificationsJobs(jobs, queue)
    expect(queue.testMode.jobs.length).to.equal(2);
    expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
    expect(queue.testMode.jobs[0].data).to.eql(jobs[0]);
    expect(queue.testMode.jobs[1].type).to.equal('push_notification_code_3');
    expect(queue.testMode.jobs[1].data).to.eql(jobs[1]);
  });
});
