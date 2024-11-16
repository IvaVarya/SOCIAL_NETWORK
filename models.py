#models.py
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Float, UniqueConstraint, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import bcrypt

Base = declarative_base()

class User(Base):  # таблица пользователей
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    login = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)  # хешированное значение пароля
    mail = Column(String, nullable=False, unique=True)
    date_of_registration = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    def set_password(self, password: str):
        # генерация хеша пароля
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password: str) -> bool:
        # проверка
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def __repr__(self):
        return f"<User(first_name={self.first_name}, last_name={self.last_name}, login={self.login},  mail={self.mail})>" 
    






    

# class UserInfo(Base):  # таблица с информацией о пользователях
#     __tablename__ = 'user_info'
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), unique=True, nullable=False)
#     birthday = Column(Date, nullable=False)
#     country_id = Column(Integer, ForeignKey('country.id', ondelete='SET NULL'), nullable=True)
    
#     def __repr__(self):
#         return f"<UserInfo(birthday={self.birthday}, country_id={self.country_id} )>"

# class Designer(Base):  # таблица для информации о дизайнере
#     __tablename__ = 'designer'
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
#     name = Column(String, nullable=False)
#     resource_id = Column(Integer, ForeignKey('resource.id', ondelete='SET NULL'), nullable=True)
#     country_id = Column(Integer, ForeignKey('country.id', ondelete='SET NULL'), nullable=True)
#     experience = Column(Float, nullable=False)  # если опыт в годах
    
#     def __repr__(self):
#         return f"<Designer(user_id={self.user_id}, name={self.name}, resource_id={self.resource_id}, country_id={self.country_id}, experience={self.experience})>"

# class Resource(Base):  # таблица для ресурсов (приложение и никнейм) для контактов
#     __tablename__ = 'resource'
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name_of_application = Column(String(100), nullable=False)  # Ограничьте длину строки
#     nickname = Column(String(100), nullable=False)
    
#     def __repr__(self):
#         return f"<Resource(name_of_application={self.name_of_application}, nickname={self.nickname})>"

# class Contact(Base):  # таблица для контактов
#     __tablename__ = 'contact'
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     manufacturer_id = Column(Integer, ForeignKey('manufacturer.id', ondelete='CASCADE'), nullable=False)
#     resource_id = Column(Integer, ForeignKey('resource.id', ondelete='CASCADE'), nullable=False)
    
#     # Ограничение уникальности для комбинации manufacturer_id и resource_id
#     __table_args__ = (UniqueConstraint('manufacturer_id', 'resource_id', name='_manufacturer_resource_uc'),)

#     def __repr__(self):
#         return f"<Contact(manufacturer_id={self.manufacturer_id}, resource_id={self.resource_id})>"

# class Sets(Base):  # таблица для наборов
#     __tablename__ = 'sets'
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     type = Column(String(100), nullable=False)  # Ограничьте длину строки
#     manufacturer_id = Column(Integer, ForeignKey('manufacturer.id', ondelete='SET NULL'), nullable=True)
#     technique_id = Column(Integer, ForeignKey('technique.id', ondelete='SET NULL'), nullable=True)
#     types_of_printed_schemes_id = Column(Integer, ForeignKey('types_of_printed_schemes.id', ondelete='SET NULL'), nullable=True)
#     fabrics_id = Column(Integer, ForeignKey('fabrics.id', ondelete='SET NULL'), nullable=True)
#     threads_id = Column(Integer, ForeignKey('threads.id', ondelete='SET NULL'), nullable=True)
#     country_id = Column(Integer, ForeignKey('country.id', ondelete='SET NULL'), nullable=True)
#     number_of_colors = Column(Integer, nullable=False)
#     number_of_mixed_colors = Column(Integer, nullable=False)
#     equipment = Column(String(255), nullable=False)
#     size_of_the_work_centimeters = Column(String(50), nullable=False)  # Можно использовать строку для формата "30x40"
#     package_size_centimeters = Column(String(50), nullable=False)
#     package_weight_grams = Column(Float, nullable=False)
#     electronic_scheme = Column(Boolean, nullable=False)
#     filling_type_id = Column(Integer, ForeignKey('filling_type.id', ondelete='SET NULL'), nullable=True)
#     description_of_sets = Column(String(500), nullable=False)

#     # Добавить уникальность для нужных полей, если нужно
#     __table_args__ = (UniqueConstraint('type', 'manufacturer_id', name='_type_manufacturer_uc'),)
    
#     def __repr__(self):
#         return f"<Sets(type={self.type}, manufacturer_id={self.manufacturer_id}, technique_id={self.technique_id}, types_of_printed_schemes_id={self.types_of_printed_schemes_id}, fabrics_id={self.fabrics_id}, threads_id={self.threads_id}, country_id={self.country_id}, number_of_colorsd={self.number_of_colors}, number_of_mixed_colors={self.number_of_mixed_colors}, equipment={self.equipment}, size_of_the_work_centimeters={self.size_of_the_work_centimeters}, package_size_centimeters={self.package_size_centimeters}, package_weight_grams={self.package_weight_grams}, electronic_scheme={self.electronic_scheme}, filling_type_id={self.filling_type_id}, description={self.description_of_sets})>"

# class DesignerSet(Base):  # таблица для связи дизайнера и его набора
#     __tablename__ = 'designer_set'
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     sets_id = Column(Integer, ForeignKey('sets.id', ondelete='CASCADE'), nullable=False)
#     designer_id = Column(Integer, ForeignKey('designer.id', ondelete='CASCADE'), nullable=False)
    
#     __table_args__ = (UniqueConstraint('sets_id', 'designer_id', name='_sets_designer_uc'),)
    
#     def __repr__(self):
#         return f"<DesignerSet(sets_id={self.sets_id}, designer_id={self.designer_id})>"

# class Country(Base):  # таблица для стран
#     __tablename__ = 'country'
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     country_name = Column(String(100), nullable=False, unique=True)  # Ограничьте длину строки
    
#     def __repr__(self):
#         return f"<Country(country_name={self.country_name})>"

# class Manufacturer(Base):  # таблица для производителей
#     __tablename__ = 'manufacturer'
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name_rus = Column(String(100), nullable=False)  # Ограничьте длину строки
#     name_eng = Column(String(100), nullable=False)  # Ограничьте длину строки
#     description_of_manufacturer = Column(String(500), nullable=False)  # Ограничьте длину строки
#     country_id = Column(Integer, ForeignKey('country.id'), nullable=False)
#     trademark = Column(String(100), nullable=False)  # Ограничьте длину строки
    
#     def __repr__(self):
#         return f"<Manufacturer(name_rus={self.name_rus}, name_eng={self.name_eng}, description_of_manufacturer={self.description_of_manufacturer}, country_id={self.country_id}, trademark={self.trademark})>"

# class Threads(Base): # таблица для ниток
#     __tablename__ = 'threads'
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     color_number = Column(Integer, nullable=False)
#     type = Column(String, nullable=False)
#     colour_rus = Column(String, nullable=False)
#     colour_eng = Column(String, nullable=False)
#     manufacturer_id = Column(Integer, ForeignKey('manufacturer.id'), nullable=False)
#     structure = Column(String, nullable=False)
#     country_id = Column(Integer, ForeignKey('country.id'), nullable=False)
#     comment = Column(String, nullable=False)
#     photo = Column(String, nullable=False)

    
#     def __repr__(self):
#         return f"<Threads(color_number={self.color_number}, type={self.type}, colour_rus={self.colour_rus}, colour_eng={self.colour_eng}, manufacturer_id={self.manufacturer_id}, structure={self.structure}, country_id={self.country_id}, comment={self.comment}, photo={self.photo})>"

# class SimilarColors(Base): # таблица для похожих цветов
#     __tablename__ = 'similar_colors'
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     original = Column(String, nullable=False)
#     selection = Column(String, nullable=False)
#     source = Column(String, nullable=False)

#     def __repr__(self):
#         return f"<SimilarColors(original={self.original}, selection={self.selection}, source={self.source})>"
  
# class Count(Base):  # таблица для стран
#     __tablename__ = 'count'
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     number_of_count = Column(Integer, nullable=False)
    
#     def __repr__(self):
#         return f"<Country(number_of_count={self.number_of_count})>"

# class Fabrics(Base): # таблица для тканей (канвы)
#      __tablename__ = 'fabrics'
     
#      id = Column(Integer, primary_key=True, autoincrement=True)
#      type_of_fabrics_id = Column(Integer, ForeignKey('type_of_fabrics.id'), nullable=False)
#      manufacturer_id = Column(Integer, ForeignKey('manufacturer.id'), nullable=False)
#      article_number = Column(Integer, nullable=False)
#      colour_rus = Column(String, nullable=False)
#      colour_eng = Column(String, nullable=False)
#      structure = Column(String, nullable=False)
#      country_id = Column(Integer, ForeignKey('country.id'), nullable=False)
#      comment = Column(String, nullable=False)
#      count_id = Column(Integer, ForeignKey('count.id'), nullable=False)
#      photo = Column(String, nullable=False)
#      name_rus = Column(String, nullable=False)
#      name_eng = Column(String, nullable=False)

#      def __repr__(self):
#         return f"<Fabrics(type_of_fabrics_id={self.type_of_fabrics_id}, manufacturer_id={self.manufacturer_id}, article_number={self.article_number}, colour_rus={self.colour_rus}, colour_eng={self.colour_eng}, structure={self.structure}, country_id={self.country_id}, comment={self.comment}, count_id={self.count_id}, photo={self.photo}, name_rus={self.name_rus}, name_eng={self.name_eng})>"

# class TypeOfFabrics(Base): # таблица для видов тканей (канвы/основы)
#      __tablename__ = 'type_of_fabrics'
     
#      id = Column(Integer, primary_key=True, autoincrement=True)
#      name_of_type_of_fabrics_rus = Column(String, nullable=False)
#      name_of_type_of_fabrics_eng = Column(String, nullable=False)
#      description_of_type_of_fabrics = Column(String, nullable=False)

#      def __repr__(self):
#         return f"<TypeOfFabrics(name_of_type_of_fabrics_rus={self.name_of_type_of_fabrics_rus}, name_of_type_of_fabrics_eng={self.name_of_type_of_fabrics_eng}, description_of_type_of_fabrics={self.description_of_type_of_fabrics})>"

# class TypesOfPalettes(Base): # таблица для видов палитр
#      __tablename__ = 'types_of_palettes'
     
#      id = Column(Integer, primary_key=True, autoincrement=True)
#      name_of_the_palette_rus = Column(String, nullable=False)
#      name_of_the_palette_eng = Column(String, nullable=False)
#      manufacturer_id = Column(Integer, ForeignKey('manufacturer.id'), nullable=False)

#      def __repr__(self):
#         return f"<TypesOfPalettes(name_of_the_palette_rus={self.name_of_the_palette_rus}, name_of_the_palette_eng={self.name_of_the_palette_eng}, manufacturer_id={self.manufacturer_id})>"
     
# class Palette(Base): # таблица для палитр
#      __tablename__ = 'palette'
     
#      id = Column(Integer, primary_key=True, autoincrement=True)
#      authors_scheme_id =  Column(Integer, ForeignKey('authors_scheme.id'), nullable=False)
#      types_of_palettes_id = Column(Integer, ForeignKey('types_of_palettes.id'), nullable=False)

#      def __repr__(self):
#         return f"<Palette(authors_scheme_id={self.authors_scheme_id}, types_of_palettes_id={self.types_of_palettes_id})>"
     
# class AuthorsScheme(Base): # таблица для авторских схем
#      __tablename__ = 'authors_scheme'
     
#      id = Column(Integer, primary_key=True, autoincrement=True)
#      designer_id = Column(Integer, ForeignKey('designer.id'), nullable=False)
#      stitch_size = Column(Integer, nullable=False)
#      number_of_colors = Column(Integer, nullable=False)
#      number_of_mixed_colors = Column(Integer, nullable=False)

#      def __repr__(self):
#         return f"<AuthorsScheme(designer_id={self.designer_id}, stitch_size={self.stitch_size}, number_of_colors={self.number_of_colors}, number_of_mixed_colors={self.number_of_mixed_colors})>"
     
# class RequiredThreads(Base): # таблица для требуемых ниток
#      __tablename__ = 'required_threads'
     
#      id = Column(Integer, primary_key=True, autoincrement=True)
#      authors_scheme_id =  Column(Integer, ForeignKey('authors_scheme.id'), nullable=False)
#      threads_id = Column(Integer, ForeignKey('threads.id'), nullable=False)
#      quantity = Column(Integer, nullable=False)

#      def __repr__(self):
#         return f"<RequiredThreads(authors_scheme_id={self.authors_scheme_id}, threads_id={self.threads_id}, quantity={self.quantity})>"
     
# class TypesOfTechniquesAuthorsSchemes(Base): # таблица для видов техник вышивания авторских наборов
#      __tablename__ = 'types_of_techniques_authors_schemes'
     
#      id = Column(Integer, primary_key=True, autoincrement=True)
#      authors_scheme_id =  Column(Integer, ForeignKey('authors_scheme.id'), nullable=False)
#      technique_id = Column(Integer, ForeignKey('technique.id'), nullable=False)
#      number_of_stitches = Column(Integer, nullable=False)

#      def __repr__(self):
#         return f"<TypesOfTechniquesAuthorsSchemes(authors_scheme_id={self.authors_scheme_id}, technique_id={self.technique_id}, number_of_stitches={self.number_of_stitches})>"

# class SetsAuthorsSchemes(Base): # таблица для наборов созданных по авторским схемам
#      __tablename__ = 'sets_authors_schemes'
     
#      id = Column(Integer, primary_key=True, autoincrement=True)
#      authors_scheme_id = Column(Integer, ForeignKey('authors_scheme.id'), nullable=False)
#      sets_id = Column(Integer, ForeignKey('sets.id'), nullable=False)

#      def __repr__(self):
#         return f"<SetsAuthorsSchemes(authors_scheme_id={self.authors_scheme_id}, sets_id={self.sets_id})>"
     
# class Technique(Base): # таблица для описания техники вышивания
#      __tablename__ = 'technique'
     
#      id = Column(Integer, primary_key=True, autoincrement=True)
#      name_of_technique_rus = Column(String, nullable=False)
#      name_of_technique_eng = Column(String, nullable=False)
#      description_of_technique = Column(String, nullable=False)

#      def __repr__(self):
#         return f"<Technique(name_of_technique_rus={self.name_of_technique_rus}, name_of_technique_eng={self.name_of_technique_eng}, description_of_technique={self.description_of_technique})>"

# class TypesOfTechniquesSets(Base): # таблица для видов техники вышивания обычных наборов
#      __tablename__ = 'types_of_techniques_sets'
     
#      id = Column(Integer, primary_key=True, autoincrement=True)
#      sets_id = Column(Integer, ForeignKey('sets.id'), nullable=False)
#      technique_id = Column(Integer, ForeignKey('technique.id'), nullable=False)
     
#      def __repr__(self):
#         return f"<TypesOfTechniquesSets(sets_id={self.sets_id}, technique_id={self.technique_id})>"
     
# class TypesOfPrintedSchemes(Base): # таблица для видов печатных схем для вышивания
#     __tablename__ = 'types_of_printed_schemes'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name_of_printed_schemes = Column(String, nullable=False)
#     description_of_printed_schemes = Column(String, nullable=False)
    
#     def __repr__(self):
#         return f"<TypesOfPrintedSchemes(name_of_printed_schemes={self.name_of_printed_schemes}, description_of_printed_schemes={self.description_of_printed_schemes})>"

# class Plot(Base): # таблица для описания сюжета
#     __tablename__ = 'plot'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name_of_plot = Column(String, nullable=False)
#     plot_description = Column(String, nullable=False)

#     def __repr__(self):
#         return f"<Plot(name_of_plot={self.name_of_plot}, plot_description={self.plot_description})>"
    
# class PlotOfEmbroidery(Base): # таблица для описания сюжета вышивки
#     __tablename__ = 'plot_of_embroidery'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     sets_id = Column(Integer, ForeignKey('sets.id'), nullable=False)
#     plot_id = Column(Integer, ForeignKey('plot.id'), nullable=False)

#     def __repr__(self):
#         return f"<PlotOfEmbroidery(sets_id={self.sets_id}, plot_id={self.plot_id})>"

# class FillingType(Base): # таблица для типа заполнения (частичное/полное)
#     __tablename__ = 'filling_type'
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name_of_filling_type = Column(String, nullable=False)
#     description_of_filling_type = Column(String, nullable=False)

#     def __repr__(self):
#         return f"<FillingType(name_of_filling_type={self.name_of_filling_type}, description_of_filling_type={self.description_of_filling_type})>"
        
# class UseOfElectronicCircuits(Base): # таблица использования электронной схемы
#     __tablename__ = 'use_of_electronic_circuits'
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     sets_id = Column(Integer, ForeignKey('sets.id'), nullable=False)
#     electronic_circuits_id = Column(Integer, ForeignKey('electronic_circuits.id'), nullable=False)
#     comment = Column(String, nullable=False)
#     manufacturer_id = Column(Integer, ForeignKey('manufacturer.id'), nullable=False)


#     def __repr__(self):
#         return f"<UseOfElectronicCircuits(sets_id={self.sets_id}, electronic_circuits_id={self.electronic_circuits_id}, comment={self.comment}, manufacturer_id={self.manufacturer_id})>"

# class ElectronicCircuits(Base): # таблица электронные схемы
#     __tablename__ = 'electronic_circuits'
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     electronic_circuit_format_id = Column(Integer, ForeignKey('electronic_circuit_format.id'), nullable=False)
#     software_id = Column(Integer, ForeignKey('software.id'), nullable=False)
#     comment = Column(String, nullable=False)

#     def __repr__(self):
#         return f"<ElectronicCircuits(format_id={self.format_id}, software_id={self.software_id}, comment={self.comment})>"

# class ElectronicCircuitFormat(Base): # таблица для форматов электронной схемы
#     __tablename__ = 'electronic_circuit_format'
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name_of_electronic_circuit_format_rus = Column(String, nullable=False)
#     name_of_electronic_circuit_format_eng = Column(String, nullable=False)
#     description_of_electronic_circuit_format = Column(String, nullable=False)

#     def __repr__(self):
#         return f"<ElectronicCircuitFormat(name_of_electronic_circuit_format_rus={self.name_of_electronic_circuit_format_rus}, name_of_electronic_circuit_format_eng={self.name_of_electronic_circuit_format_eng}, description_of_electronic_circuit_format={self.description_of_electronic_circuit_format})>"

# class Software(Base): # таблица для программных обеспечений
#     __tablename__ = 'software'
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name_of_software_rus = Column(String, nullable=False)
#     name_of_software_eng = Column(String, nullable=False)
#     description_of_software = Column(String, nullable=False)
#     manufacturer_id = Column(Integer, ForeignKey('manufacturer.id'), nullable=False)

#     def __repr__(self):
#         return f"<Software(name_of_software_rus={self.name_of_software_rus}, name_of_software_eng={self.name_of_software_eng}, description_of_software={self.description_of_software}, manufacturer_id={self.manufacturer_id})>"

# class Platform(Base): # таблица для платформы
#     __tablename__ = 'platform'
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     software_id = Column(Integer, ForeignKey('software.id'), nullable=False)
#     types_of_platforms_id = Column(Integer, ForeignKey('types_of_platforms.id'), nullable=False)
#     comment = Column(String, nullable=False)

#     def __repr__(self):
#         return f"<Platform(software_id={self.software_id}, types_of_platforms_id={self.types_of_platforms_id}, comment={self.comment})>"

# class TypesOfPlatforms(Base): # таблица для типов платформ
#     __tablename__ = 'types_of_platforms'
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name_of_platform_rus = Column(String, nullable=False)
#     name_of_platform_eng = Column(String, nullable=False)
#     description_of_platform = Column(String, nullable=False)

#     def __repr__(self):
#         return f"<TypesOfPlatforms(name_of_platform_rus={self.name_of_platform_rus}, name_of_platform_eng={self.name_of_platform_eng}, description_of_platform={self.description_of_platform})>"














# class Favourites(Base):  # таблица для избранного 
#     __tablename__ = 'favourites'
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
#     date_of_addition = Column(DateTime, nullable=False)
#     unit = Column(String, nullable=False)
#     date_of_deletion = Column(DateTime, nullable=True)  # может быть необязательно
    
#     def __repr__(self):
#         return f"<Favourites(unit={self.unit}, date_of_addition={self.date_of_addition})>"


# class Reserves(Base):  # таблица для запасов
#     __tablename__ = 'reserves'
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
#     date_of_addition = Column(DateTime, nullable=False)
#     unit = Column(String, nullable=False)
#     date_of_deletion = Column(DateTime, nullable=True)  # может быть необязательно
    
#     def __repr__(self):
#         return f"<Reserves(unit={self.unit}, date_of_addition={self.date_of_addition})>"
    

    
