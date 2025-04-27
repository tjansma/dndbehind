Okay, here is the revised set of User Stories, Functional Requirements, and Non-Functional Requirements, expanded to include the goal of covering D&D 5E SRD content related to character and inventory management, based on the provided backend documentation and the SRD details found.

*(Note: "Implemented Backend" indicates the core API endpoint and database models likely exist based on the initial documentation. "Partially Implemented Backend" means some related structures exist, but significant expansion is needed. Most SRD-specific features are assumed to be Not Implemented yet).*

## User Roles Identified

* **Player:** A standard user who manages their D&D characters.
* **Administrator:** A user with privileges to manage users and roles.
* **Maintainer:** A user with privileges to manage shared SRD game content (Backgrounds, potentially SRD Equipment/Races/Classes if editable).
* **Operator:** (Implied by `get_character` permission) A user with broader read access.

## User Stories

**Player Stories**

* **Account Management:**
    * As a Player, I want to register for a new account using my email and a password, so that I can start using the application. *(US-P01)*
    * As a Player, I want to log in securely using my username and password, so that I can access my characters and data. *(US-P02)*
    * As a Player, I want the system to keep me logged in via a secure token, so that I don't have to log in repeatedly. *(US-P03)*
    * As a Player, I want to view my user profile information, so that I know how I am identified in the system. *(US-P04)*
* **Character Creation:**
    * As a Player, I want to start creating a new D&D 5E character, so that I can play the game. *(US-P05)*
    * As a Player, I want to choose a method for determining ability scores (e.g., Standard Array, Point Buy) during character creation, so that I can define my character's core stats. *(US-P06)*
    * As a Player, I want to assign generated or purchased ability scores (Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma) to my character. *(US-P07)*
    * As a Player, I want to select a race from the available SRD options (e.g., Dwarf, Elf, Human), so that my character gains racial traits and ability score increases. *(US-P08)*
    * As a Player, I want to select a class from the available SRD options (e.g., Fighter, Wizard), so that my character gains class features, proficiencies, and hit dice. *(US-P09)*
    * As a Player, I want the system to automatically calculate my character's starting Hit Points based on my chosen class and Constitution modifier. *(US-P10)*
    * As a Player, I want to choose my character's skill proficiencies based on options provided by my class and background. *(US-P11)*
    * As a Player, I want to select starting equipment either by choosing an SRD equipment pack (e.g., Explorer's Pack) or by using starting wealth based on my class, so that my character is equipped for adventure. *(US-P12)*
    * As a Player, I want to select a Background from the available list based on SRD content, so that my character gains background features, proficiencies, and starting equipment/gold. *(US-P13)*
    * As a Player, I want to define my character's descriptive details like name, alignment, age, height, weight, eye color, hair color, so that I can personalize my character. *(US-P14)*
* **Character Management & Viewing:**
    * As a Player, I want to view a list of all my characters, so that I can easily select one to view or edit. *(US-P15)*
    * As a Player, I want to view the complete details of a specific character I own, presented in a clear character sheet format, including stats, skills, proficiencies, HP, AC, equipment, inventory, features, and spells (if applicable). *(US-P16)*
    * As a Player, I want the character sheet to automatically calculate and display derived statistics (e.g., ability modifiers, skill bonuses, saving throws, passive perception, AC, initiative, attack bonuses) based on SRD rules. *(US-P17)*
    * As a Player, I want to edit the details of a character I own (e.g., stats, name, level, alignment, descriptive details), so that I can update it as my character progresses or to correct mistakes. *(US-P18)*
    * As a Player, I want to level up my character, increasing their Hit Points, gaining new class features, and potentially increasing proficiency bonus or ability scores according to SRD rules. *(US-P19)*
    * As a Player, I want to delete a character I own, so that I can remove characters I no longer need. *(US-P20)*
* **Inventory Management:**
    * As a Player, I want to view my character's inventory, including equipment, weapons, armor, tools, and other items. *(US-P21)*
    * As a Player, I want to add SRD equipment items to my character's inventory, either from purchases or found loot. *(US-P22)*
    * As a Player, I want to remove items from my character's inventory. *(US-P23)*
    * As a Player, I want to equip or unequip armor and weapons from my inventory, so that the system can calculate AC and attack bonuses correctly. *(US-P24)*
    * As a Player, I want to track the quantity of stackable items (e.g., arrows, rations, coins). *(US-P25)*
    * As a Player, I want to track my character's currency (Copper, Silver, Electrum, Gold, Platinum pieces). *(US-P26)*
    * As a Player, I want the system to calculate my character's total inventory weight based on SRD item weights. *(US-P27)*
    * As a Player, I want the system to calculate my character's carrying capacity based on their Strength score according to SRD rules, so I know if I am encumbered. *(US-P28)*
* **Usability:**
    * As a Player, I want my interactions with the character sheet (e.g., updating a stat, equipping an item) to feel responsive with immediate feedback via partial page updates (`htmx`), so the interface feels fluid. *(US-P29)*

**Administrator Stories**

* As an Administrator, I want to view a list of all registered users and their assigned roles, so that I can manage system access. *(US-A01)*
* As an Administrator, I want to assign specific roles (Player, Maintainer, Operator, Administrator) to a user, so that I can grant appropriate permissions. *(US-A02)*
* As an Administrator, I want to remove specific roles from a user, so that I can revoke permissions. *(US-A03)*
* As an Administrator, I want to disable or enable a user account, so that I can manage user access. *(US-A04)*

**Maintainer Stories**

* As a Maintainer, I want to view and manage the list of available SRD Backgrounds (create, read, update, delete), so that the information presented to players is accurate according to the SRD. *(US-M01)*
* As a Maintainer, I want to view and manage the list of available SRD Races and their traits (read-only, potentially update if interpretations change/errors found), so the character creation options are correct. *(US-M02)*
* As a Maintainer, I want to view and manage the list of available SRD Classes and their features (read-only, potentially update), so the character creation options are correct. *(US-M03)*
* As a Maintainer, I want to view and manage the list of available SRD Equipment items (read-only, potentially update), so the inventory options are correct. *(US-M04)*

**Operator Stories**

* As an Operator, I want to view the details of any character (not just my own), so that I can provide support or perform oversight tasks. *(US-O01)*

## Functional Requirements

*(Backend Status based on `dndbehind_documentation.md`)*

**Authentication & Authorization**

* FR01: The system **shall** allow new users to register with a unique username, unique email, and password. *(Implemented Backend)*
* FR02: The system **shall** securely hash user passwords using Argon2. *(Implemented Backend)*
* FR03: The system **shall** allow registered users to log in using their username and password. *(Implemented Backend)*
* FR04: Upon successful login, the system **shall** generate a JSON Web Token (JWT) containing user ID and roles. *(Implemented Backend)*
* FR05: The system **shall** return the JWT to the authenticated user. *(Implemented Backend)*
* FR06: The system **shall** require a valid JWT for accessing protected endpoints. *(Implemented Backend)*
* FR07: The frontend **shall** store the received JWT securely (e.g., in an `HttpOnly` cookie managed by the frontend server). *(Not Implemented)*
* FR08: The frontend **shall** send the JWT with subsequent requests to the backend API. *(Not Implemented)*
* FR09: The backend API **shall** validate the JWT signature and expiration on protected requests. *(Implemented Backend)*
* FR10: The system **shall** provide an endpoint to retrieve the current logged-in user's information based on their JWT. *(Implemented Backend)*
* FR11: The system **shall** implement Role-Based Access Control (RBAC) using roles: 'Player', 'Administrator', 'Maintainer', 'Operator'. *(Implemented Backend - Roles exist, specific set might need adjustment)*
* FR12: The system **shall** allow Administrators to list all users and their roles. *(Implemented Backend)*
* FR13: The system **shall** allow Administrators to assign roles to users. *(Implemented Backend)*
* FR14: The system **shall** allow Administrators to remove roles from users. *(Implemented Backend)*
* FR15: The system **shall** restrict access to resources based on assigned roles and resource ownership. *(Implemented Backend - Decorators exist)*
* FR16: The backend **shall** track the last login time for users. *(Implemented Backend)*
* FR17: The system **shall** handle disabled user accounts during login. *(Partially Implemented Backend - Implied by auth flows)*

**Character Data Model (SRD Focus)**

* FR20: The Character model **shall** include fields for: name, level, alignment, age, height, weight, eye color, hair color, player (owner ID), race, class(es), background. *(Partially Implemented Backend - Character model exists, needs fields)*
* FR21: The Character model **shall** store 6 base ability scores: Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma. *(Partially Implemented Backend - Character model exists, needs fields, type fix mentioned)*
* FR22: The system **shall** store proficiency selections for skills, saving throws, weapons, armor, and tools based on race, class, and background choices. *(Not Implemented)*
* FR23: The Character model **shall** store current Hit Points (HP) and maximum HP. *(Not Implemented)*
* FR24: The Character model **shall** store temporary Hit Points. *(Not Implemented)*
* FR25: The Character model **shall** store Hit Dice (total and remaining by type). *(Not Implemented)*
* FR26: The system **shall** store known languages based on race and background. *(Not Implemented)*
* FR27: The system **shall** store character speed based on race. *(Not Implemented)*
* FR28: The system **shall** store special senses (e.g., Darkvision) based on race. *(Not Implemented)*
* FR29: The system **shall** represent and store class-specific features gained at each level according to SRD rules (e.g., Rage uses for Barbarian, Spell Slots for Wizard). *(Not Implemented)*

**SRD Content Implementation**

* FR30: The system **shall** implement data models and logic for SRD Races (Dwarf, Elf, Halfling, Human, Dragonborn, Gnome, Half-Elf, Half-Orc, Tiefling), including their traits, ability score modifiers, speed, senses, and languages. *(Not Implemented)*
* FR31: The system **shall** implement data models and logic for SRD Classes (Barbarian, Bard, Cleric, Druid, Fighter, Monk, Paladin, Ranger, Rogue, Sorcerer, Warlock, Wizard), including their hit dice, proficiencies (saving throws, skills, armor, weapons, tools), starting equipment options, and features gained at levels 1-20 according to the SRD. *(Not Implemented)*
* FR32: The system **shall** implement data models for SRD Backgrounds, including skill proficiencies, tool proficiencies, languages, starting equipment/gold, and features. *(Partially Implemented Backend - Background model exists)*
* FR33: The system **shall** implement the list of SRD Skills and associate them with their corresponding ability scores (e.g., Athletics -> Strength). *(Not Implemented)*
* FR34: The system **shall** implement SRD Equipment items (Adventuring Gear, Armor, Weapons, Tools), including their cost, weight, and relevant properties (AC for armor, damage/type for weapons). *(Not Implemented)*
* FR35: The system **shall** implement SRD starting Equipment Packs (Burglar's, Diplomat's, Dungeoneer's, etc.). *(Not Implemented)*

**Character Creation & Management**

* FR40: The system **shall** guide the Player through the character creation steps: Ability Scores, Race selection, Class selection, Background selection, Skill/Proficiency selection, Equipment selection, Descriptive details. *(Not Implemented)*
* FR41: The system **shall** support standard methods for ability score generation (e.g., Standard Array, Point Buy). *(Not Implemented)*
* FR42: The system **shall** apply racial ability score modifiers correctly. *(Not Implemented)*
* FR43: The system **shall** allow selection of skill/tool proficiencies granted by Race, Class, and Background from valid options. *(Not Implemented)*
* FR44: The system **shall** provide options for starting equipment (class/background packs or starting gold based on class). *(Not Implemented)*
* FR45: The system **shall** allow authenticated Players to create new characters, saving all selected and calculated data. *(Backend model exists, endpoint needed)*
* FR46: The system **shall** allow a Player to view a list of characters they own. *(Not Implemented)*
* FR47: The system **shall** allow a Player or an Operator to retrieve the full details of a specific character. *(Implemented Backend endpoint for GET)*
* FR48: The system **shall** allow a Player to update the details (name, stats, level, description etc.) of a character they own. *(Not Implemented)*
* FR49: The system **shall** allow a Player to delete a character they own. *(Not Implemented)*
* FR50: The system **shall** implement character leveling up, including increasing max HP (rolling hit dice or taking average), gaining new class features, and tracking proficiency bonus increases. *(Not Implemented)*
* FR51: The system **shall** enforce SRD rules and prerequisites during character creation and leveling (e.g., multiclassing prerequisites). *(Not Implemented)*

**Calculations & Derived Stats**

* FR60: The system **shall** calculate ability score modifiers based on ability scores. *(Not Implemented)*
* FR61: The system **shall** calculate skill bonuses (Ability Modifier + Proficiency Bonus if proficient). *(Not Implemented)*
* FR62: The system **shall** calculate saving throw bonuses (Ability Modifier + Proficiency Bonus if proficient). *(Not Implemented)*
* FR63: The system **shall** calculate Passive Perception (10 + Perception skill bonus). *(Not Implemented)*
* FR64: The system **shall** calculate Armor Class (AC) based on equipped armor, shields, Dexterity modifier, and other applicable features (e.g., Unarmored Defense). *(Not Implemented)*
* FR65: The system **shall** calculate Initiative bonus (Dexterity modifier). *(Not Implemented)*
* FR66: The system **shall** calculate attack and damage bonuses for equipped weapons based on relevant ability scores (Strength or Dexterity) and proficiency bonus. *(Not Implemented)*
* FR67: The system **shall** calculate character carrying capacity based on Strength score (Strength score x 15 pounds per SRD). *(Not Implemented)*
* FR68: The system **shall** calculate the total weight of the character's inventory. *(Not Implemented)*
* FR69: The system **shall** indicate if a character is encumbered based on inventory weight vs. carrying capacity (optional SRD variant rule, consider if implementing). *(Not Implemented)*

**Inventory Management**

* FR70: The system **shall** allow Players to view their character's inventory, categorized (e.g., Weapons, Armor, Gear). *(Not Implemented)*
* FR71: The system **shall** allow Players to add/remove items from the SRD equipment list to/from their inventory. *(Not Implemented)*
* FR72: The system **shall** allow Players to manage quantities for stackable items. *(Not Implemented)*
* FR73: The system **shall** allow Players to equip/unequip armor, shields, and weapons. *(Not Implemented)*
* FR74: The system **shall** track currency (CP, SP, EP, GP, PP) for each character. *(Not Implemented)*
* FR75: The system **shall** deduct currency when items are "purchased" (if implementing starting wealth or shopping). *(Not Implemented)*
* FR76: The system **shall** enforce inventory limits based on carrying capacity/encumbrance rules if implemented. *(Not Implemented)*

**Content Management (SRD)**

* FR80: The system **shall** allow Maintainers to create new character Backgrounds with a unique name and description. *(Implemented Backend)*
* FR81: The system **shall** allow Maintainers to list all available Backgrounds. *(Implemented Backend)*
* FR82: The system **shall** allow Maintainers to update existing Backgrounds. *(Not Implemented)*
* FR83: The system **shall** allow Maintainers to delete existing Backgrounds. *(Not Implemented)*
* FR84: Players **shall** be able to view and select from the list of available SRD Backgrounds. *(Partially Implemented - List endpoint exists, selection UI needed)*
* FR85: The system **shall** provide read access (potentially managed by Maintainers) to SRD Race, Class, Skill, and Equipment data used by the application logic. *(Not Implemented)*

**Frontend Interaction (`htmx`)**

* FR90: User interactions on the character sheet (e.g., editing a stat, equipping an item) **shall** trigger partial page updates using `htmx`. *(Not Implemented)*
* FR91: Forms submitted via `htmx` **shall** provide validation feedback inline or near the relevant fields without a full page reload. *(Not Implemented)*
* FR92: Changes to core character data (e.g., ability score, level, equipped items) **shall** trigger `htmx` updates to all dependent calculated fields (e.g., modifiers, skills, AC, attack bonuses, carrying capacity) displayed on the sheet. *(Not Implemented)*
* FR93: The frontend **shall** provide visual indicators during `htmx` requests. *(Not Implemented)*

## Non-Functional Requirements

*(Largely unchanged, but re-iterated for completeness)*

**Performance**

* NFR01: Backend API responses **shall** typically complete within 500ms under normal load.
* NFR02: Frontend partial page updates via `htmx` **shall** feel responsive, aiming for completion within 1 second (including server processing and network latency).
* NFR03: The system **shall** be able to support at least 50 concurrent users interacting with character sheets without significant degradation (initial target).

**Scalability**

* NFR04: Both frontend and backend server components **shall** be stateless to allow for easy horizontal scaling. *(Backend designed, Frontend planned)*
* NFR05: The system architecture **shall** support running multiple instances of the frontend and backend containers behind load balancers.

**Reliability**

* NFR06: The system **shall** aim for 99.9% uptime for core functionality (excluding scheduled maintenance).
* NFR07: Database migrations **shall** be handled reliably using Flask-Migrate/Alembic. *(Implemented Backend)*
* NFR08: Application errors **shall** be logged appropriately for troubleshooting. *(Partially Implemented Backend)*

**Security**

* NFR09: All communication between the client, frontend server, and backend API **shall** use HTTPS in production.
* NFR10: Sensitive configuration (secret keys, database URLs) **shall** be managed via environment variables or secrets management. *(Implemented Backend)*
* NFR11: JWTs **shall** have reasonably short expiration times. (Refresh tokens TBD). *(JWT expiration mentioned)*
* NFR12: Input data **shall** be validated on the server-side. *(Partially Implemented Backend)*
* NFR13: Appropriate CORS policies **shall** be configured for the backend API in production.
* NFR14: Frontend JWT storage **shall** use `HttpOnly`, `Secure` cookies managed by the frontend server.

**Usability**

* NFR15: The character creation process **shall** be guided and intuitive.
* NFR16: The character sheet display **shall** be clear, readable, and logically organized, presenting all relevant SRD information.
* NFR17: Error messages displayed to the user **shall** be clear and helpful.

**Maintainability**

* NFR18: Code **shall** follow PEP 8 guidelines and include type hints and docstrings. *(Best practice stated)*
* NFR19: The codebase **shall** be modular (separate frontend/backend repos recommended). *(Backend structure exists)*
* NFR20: Automated tests **shall** be implemented for both frontend and backend with high code coverage targets (>80%). *(Implemented Backend testing structure)*
* NFR21: The system **shall** be well-documented. *(Partially Implemented)*

**Deployment**

* NFR22: Both frontend and backend applications **shall** be deployable as Docker containers. *(Implemented Backend Dockerfile)*
* NFR23: A CI/CD pipeline **shall** automate testing, building images, and potentially deployment. *(Implemented Backend CI config skeletons)*
* NFR24: The deployment architecture **shall** follow the specified design (DB internal, API/FE in DMZ).

This revised list should provide a much more comprehensive scope covering the D&D 5E SRD character and inventory management aspects for your project.
