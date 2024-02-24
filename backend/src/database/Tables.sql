--  CATEGORY: User
CREATE TABLE "User" (
  "Uid" SERIAL PRIMARY KEY, --serial zorgt dat het id nummer automatisch gegenereert wordt
  "UserName" text,
  "EMail" text UNIQUE,
  "PassWord" text,
  "FactionName" text,
  "Clan" text REFERENCES Clan ("Name")
);

--  CATEGORY: Interaction

-- Clan = groep van users, deze vormen een alliance en hebben een groepschat
CREATE TABLE "Clan" (
  "Name" text PRIMARY KEY,
  "MessageBoard" int REFERENCES MessageBoard("Bid")
);


CREATE TABLE "Message" (
  "Mid" SERIAL PRIMARY KEY,
  "SenderId" int REFERENCES "User"("Uid"),
  "MessageBoardId" int REFERENCES "MessageBoard"("Bid")
  "CreationDateTime" timestamp,
  "ParentMessageID" int REFERENCES "Message"("Mid"), -- houdt de ID bij van het bericht waarop dit bericht de respons is
  "read" bool, -- boolean geeft aan of het bericht reeds gelezen is
  "body" text
);

-- MessageBoard = een chat, elk bericht wordt in 1 bepaalde chat gepost
CREATE TABLE "MessageBoard" (
  "Bid" SERIAL PRIMARY KEY,
  "chatName" text
);

-- ReaderOf = deze table bepaalt welke users welke chats kunnen lezen
CREATE TABLE "ReaderOf" (
    "BoardId" int REFERENCES "MessageBoard"("Bid"),
    "UserId" int REFERENCES "User"("Uid")
);




-- CATEGORY: Geographical layout
CREATE TABLE "SpaceRegion" (
  "Id" SERIAL PRIMARY KEY,
  "Name" text UNIQUE NOT NULL
);

-- een type planeet heeft bepaalde eigenschappen
-- normaal zouden bepaalde resources meer prevalent zijn
-- dit moet echter nog meer uitgewerkt worden wanneer de resources geïmplementeerd worden
CREATE TABLE "Planet" (
  "Id" SERIAL PRIMARY KEY,
  "Name" text UNIQUE NOT NULL,
  "PlanetType" text REFERENCES "PlanetType"("type"),
  "RegionId" int REFERENCES "SpaceRegion"("Id")
);

-- relatie tussen regiontype en resources die prevalent zijn moet nog uitgewerkt worden (valt onder properties)
CREATE TABLE "PlanetType" (
  "type" text,
  "properties" text
);

CREATE TABLE "Gate" (
  "ID" SERIAL PRIMARY KEY,
  "From" text NOT NULL REFERENCES "Planet"("Name"),
  "To" text NOT NULL REFERENCES "Planet"("Name"),
  CONSTRAINT "Unique_Gate_From_To" UNIQUE ("From", "To")
);

CREATE TABLE "PlanetRegion" (
  "Id" SERIAL,
  "PlanetId" int REFERENCES "Planet"("Id"),
  "regionType" text REFERENCES "PlanetRegionType"("Type"),
  "ControlledBy" text REFERENCES "User"("FactionName"),
  PRIMARY KEY ("PlanetId", "Id")
);

CREATE TABLE "PlanetRegionType" (
  "Type" varchar PRIMARY KEY,
  "properties" text
);

CREATE TABLE "City" (
  "Id" SERIAL UNIQUE,
  "RegionId" int REFERENCES "PlanetRegion"("Id"),
  "Rank" int,
  "wallId" int,
  PRIMARY KEY ("RegionId", "Id")
);





