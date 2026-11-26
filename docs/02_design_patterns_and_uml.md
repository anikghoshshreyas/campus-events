# 2. Design Patterns and UML

| Pattern | Problem solved | Alternative rejected (why) |
|---|---|---|
| Factory Method (creational) `EventFactory` | Each event kind has different defaults/validation | if/elif in routes – duplicated, hard to extend |
| Strategy (behavioral) `PricingStrategy` | Price rules change often | Conditionals in service – violates open/closed |
| Observer (behavioral) `EventBus` | Registration must trigger e-mail without coupling | Direct mailer call – service knows every consumer |
| Adapter (structural) `VendorGatewayAdapter` | Vendor SDK uses cents/tokens, incompatible interface | Calling SDK directly – vendor lock-in, untestable |

## UML class diagram (Mermaid – paste into https://mermaid.live and export PNG)
```mermaid
classDiagram
  class EventFactory { +create(kind,title,date,capacity,fee) Event }
  class PricingStrategy { <<interface>> +price(base_fee) float }
  PricingStrategy <|-- StandardPricing
  PricingStrategy <|-- StudentDiscount
  PricingStrategy <|-- EarlyBird
  class PaymentGateway { <<interface>> +pay(amount,email) PaymentResult }
  PaymentGateway <|-- VendorGatewayAdapter
  VendorGatewayAdapter o-- LegacyVendorClient
  class EventBus { +subscribe(topic,cb) +publish(topic,payload) }
  EventBus --> EmailNotifier
  class RegistrationService { +register(user_id,event_id) Registration }
  RegistrationService --> PricingStrategy
  RegistrationService --> PaymentGateway
  RegistrationService --> EventBus
  RegistrationService --> UserRepository
  RegistrationService --> EventRepository
  RegistrationService --> RegistrationRepository
  EventService --> EventFactory
  class User
  class Event
  class Registration
  Registration --> User
  Registration --> Event
```
