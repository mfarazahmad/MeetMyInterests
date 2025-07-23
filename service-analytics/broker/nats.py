import asyncio
import json
from typing import Optional, Dict, Any, Callable
from nats.aio.client import Client as NATS
from nats.aio.msg import Msg
from config.logger import log

class Broker:
    """NATS JetStream broker implementation with streaming capabilities."""
    
    def __init__(self, host: str, topic: str, group: str, timeout: int):
        """
        Initialize NATS broker connection.
        
        Args:
            host: NATS server URL (e.g., 'nats://localhost:4222')
            topic: Stream/Subject name
            group: Consumer group name (for load balancing)
            timeout: Connection timeout in seconds
        """
        self.host = host
        self.topic = topic
        self.group = group
        self.timeout = timeout
        self.nc: Optional[NATS] = None
        self.js = None
        self.subscription = None
        self._running = False
        
        log.info(f"Initializing NATS JetStream connection to {host}")
        log.info(f"Stream: {topic}, Consumer Group: {group}")
    
    async def connect(self) -> bool:
        """Establish connection to NATS server."""
        try:
            self.nc = NATS()
            
            # Connect to NATS server
            await self.nc.connect(
                servers=[self.host],
                connect_timeout=self.timeout,
                reconnect_time_wait=1,
                max_reconnect_attempts=5
            )
            
            # Get JetStream context
            self.js = self.nc.jetstream()
            
            # Ensure stream exists
            await self._ensure_stream()
            
            # Create consumer if it doesn't exist
            await self._ensure_consumer()
            
            log.info(f"Successfully connected to NATS JetStream at {self.host}")
            return True
            
        except Exception as e:
            log.error(f"Failed to connect to NATS: {e}")
            return False
    
    async def _ensure_stream(self):
        """Ensure the stream exists, create if it doesn't."""
        try:
            # Try to get stream info
            await self.js.stream_info(self.topic)
            log.info(f"Stream '{self.topic}' already exists")
        except Exception:
            # Stream doesn't exist, create it
            try:
                await self.js.add_stream(
                    name=self.topic,
                    subjects=[f"{self.topic}.*"],
                    retention="workqueue",
                    max_msgs_per_subject=1000,
                    max_age=24 * 60 * 60,  # 24 hours
                    storage="file"
                )
                log.info(f"Created stream '{self.topic}'")
            except Exception as e:
                log.error(f"Failed to create stream '{self.topic}': {e}")
                raise
    
    async def _ensure_consumer(self):
        """Ensure the consumer exists, create if it doesn't."""
        try:
            # Try to get consumer info
            await self.js.consumer_info(self.topic, self.group)
            log.info(f"Consumer '{self.group}' already exists")
        except Exception:
            # Consumer doesn't exist, create it
            try:
                await self.js.add_consumer(
                    stream=self.topic,
                    durable_name=self.group,
                    deliver_group=self.group,  # For load balancing
                    ack_policy="explicit",
                    ack_wait=30,  # 30 seconds
                    max_deliver=3,
                    filter_subject=f"{self.topic}.*"
                )
                log.info(f"Created consumer '{self.group}'")
            except Exception as e:
                log.error(f"Failed to create consumer '{self.group}': {e}")
                raise
    
    async def publish(self, subject: str, data: Dict[str, Any]) -> bool:
        """
        Publish message to NATS JetStream.
        
        Args:
            subject: Subject to publish to (will be prefixed with topic)
            data: Data to publish
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not self.js:
                log.error("Not connected to NATS")
                return False
            
            full_subject = f"{self.topic}.{subject}"
            message = json.dumps(data).encode('utf-8')
            
            ack = await self.js.publish(full_subject, message)
            log.info(f"Published message to {full_subject}, sequence: {ack.seq}")
            return True
            
        except Exception as e:
            log.error(f"Failed to publish message: {e}")
            return False
    
    async def subscribe(self, callback: Callable[[Dict[str, Any]], None]) -> bool:
        """
        Subscribe to messages with a callback function.
        
        Args:
            callback: Function to call when message is received
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not self.js:
                log.error("Not connected to NATS")
                return False
            
            # Subscribe to stream with consumer
            self.subscription = await self.js.pull_subscribe(
                subject=f"{self.topic}.*",
                durable=self.group,
                stream=self.topic
            )
            
            log.info(f"Subscribed to stream '{self.topic}' with consumer '{self.group}'")
            
            # Start listening for messages
            await self._listen_for_messages(callback)
            return True
            
        except Exception as e:
            log.error(f"Failed to subscribe: {e}")
            return False
    
    async def _listen_for_messages(self, callback: Callable[[Dict[str, Any]], None]):
        """Listen for incoming messages and process them."""
        self._running = True
        log.info(f"Listening for messages on stream '{self.topic}'")
        
        while self._running:
            try:
                # Fetch messages (pull-based)
                messages = await self.subscription.fetch(batch=1, timeout=1)
                
                for msg in messages:
                    try:
                        # Decode message
                        data = json.loads(msg.data.decode('utf-8'))
                        log.info(f"Received message: {data}")
                        
                        # Process message
                        callback(data)
                        
                        # Acknowledge message
                        await msg.ack()
                        
                    except json.JSONDecodeError as e:
                        log.error(f"Failed to decode message: {e}")
                        await msg.ack()  # Acknowledge to avoid redelivery
                        
                    except Exception as e:
                        log.error(f"Error processing message: {e}")
                        await msg.nak()  # Negative acknowledgment for retry
                
            except Exception as e:
                if self._running:
                    log.error(f"Error in message listener: {e}")
                    await asyncio.sleep(1)  # Wait before retrying
    
    async def listen(self):
        """Legacy method for backward compatibility."""
        log.warning("listen() is deprecated. Use subscribe() with callback instead.")
        
        def default_callback(data: Dict[str, Any]):
            log.info(f"Received message: {data}")
        
        await self.subscribe(default_callback)
    
    async def stop(self):
        """Stop the broker and close connections."""
        self._running = False
        
        if self.subscription:
            await self.subscription.unsubscribe()
        
        if self.nc:
            await self.nc.close()
        
        log.info("NATS broker stopped")
    
    def __del__(self):
        """Cleanup on deletion."""
        if self.nc and not self.nc.is_closed:
            asyncio.create_task(self.nc.close())

# Legacy class for backward compatibility
class KafkaConsumer:
    """Legacy class for backward compatibility."""
    
    def __init__(self, *args, **kwargs):
        log.warning("KafkaConsumer is deprecated. Use Broker class instead.")
        raise DeprecationWarning("KafkaConsumer is deprecated. Use Broker class instead.")