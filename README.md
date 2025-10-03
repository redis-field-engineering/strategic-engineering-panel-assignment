# Hot IP Detection System Assignment

## Overview

You are tasked with building a **real-time hot IP detection system** that identifies and tracks IP addresses generating high traffic volumes.

The system consists of three main components:
1. A producer that generates fake web access logs with rotating hot IPs onto a Redis Stream (provided)
2. A component that consumes the stream and track hot IPs using Redis data structures
3. A component that provides multiple analytical views of the hot IP data

It is OK to use AI for coding but please tell us when you present how you used it. You will be expected to explain the solution in addition to having it work.

## What You're Given

- Working producer that generates realistic web access logs
- Producer Docker configuration
- Requirements and detailed specifications

Sample log entry:

```json
{
  "method": "GET",
  "ip": "192.168.1.100",
  "path": "/api/users/123",
  "timestamp": "2025-10-02 14:35:42"
}
```

## Detailed Requirements

1. **Read from Redis Stream**
   - Connect to the stream created by the producer
   - Process log entries in real-time
   - Handle stream consumer groups properly

2. **Maintain Overall Hot IP Tracking**
   - Choose an appropriate Redis data structure for tracking the hottest IPs across all time periods
   - Choose an appropriate Redis data structure to maintain an overall count of all requests
   - The top N IPs will need to be retrieved and displayed
   - Store incoming IP address counts in this structure
   - Consider complexity and memory usage

3. **Maintain Time-Windowed Data**
   - Choose an appropriate Redis data structure for tracking IPs within 5-minute time windows
   - Store IP addresses with their request counts as scores
   - Consider how you will combine windows together to provide time range results
   - Consider how you will retrieve previous windows using a start time

4. **Be able to report this data in different modes (CLI)**
   - Mode 1: `--mode overall` displays overall top 10 results with percentages of total requests
   - Mode 2: `--mode recent` displays of 3 most recent 5-minute windows showing top IPs per window with counts and percentages
   - Mode 3: `--mode timerange` provides historical analysis for specific time periods. Support `--minutes N` (must be divisible by 5). Support `--start-time` with multiple date formats:
      - `2025-10-02 14:30:00` (full datetime)
      - `2025-10-02 14:30` (no seconds)
      - `2025-10-02` (date only, assumes 00:00:00)
      - `14:30` (time only, assumes today)
      - `10/02/2025 14:30` (US format)

### Docker Compose Requirements

Create a `docker-compose.yml` that includes the producer, Redis and everything you need to run your solution.

We should be able to run `docker-compose up` and see logs being generated.

Provide instructions for running and testing your solution in the README.



## Deliverables

### Code Implementation
- [ ] `docker-compose.yml` - Orchestrates all services
- [ ] consuming log data from Redis Stream into Redis data structures
- [ ] able to run report with all the required modes
- [ ] clean and well-documented code along with instructions on usage

### 3. Presentation (3-5 slides)
Prepare a short presentation covering:

#### Slide 1: Problem & Solution Overview
- What is hot IP detection and why is it important?
- High-level architecture of your solution

#### Slide 2: Technical Implementation
- Redis data structures used and why
- Key design decisions (time windows, complexity, tradeoffs, etc.)

#### Slide 3: Design for Consuming the Stream
- How you process the stream
- Overall vs. time-windowed tracking approach

#### Slide 4: Capabilities for Reporting
- The different modes and their use cases
- Demo of key functionality

#### Slide 5: Challenges & Future Improvements
- Any challenges encountered and how you solved them
- What you would improve with more time


Good luck! 🚀