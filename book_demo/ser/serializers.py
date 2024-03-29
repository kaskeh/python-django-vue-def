from rest_framework import serializers

# 所有的自定义序列化器必须直接或间接继承于 serializers.Serializer
class StudentSerializer(serializers.Serializer):
    # 声明序列化器
    # 1. 字段声明[ 要转换的字段，当然，如果写了第二部分代码，有时候也可以不用写字段声明 ]
    id = serializers.IntegerField()
    name = serializers.CharField()
    sex = serializers.BooleanField()
    age = serializers.IntegerField()
    class_null = serializers.CharField()
    description = serializers.CharField()

    # 2. 可选[ 如果序列化器继承的是ModelSerializer，则需要声明对应的模型和字段, ModelSerializer是Serializer的子类 ]

    # 3. 可选[ 用于对客户端提交的数据进行验证 ]

    # 4. 可选[ 用于把通过验证的数据进行数据库操作，保存到数据库 ]


"""
  在drf中，对于客户端提供的数据，往往需要验证数据的有效性，这部分代码是写在序列化器中的。
  在序列化器中，已经提供三个地方给我们针对客户端提交的数据进行验证。
  1. 内置选项，字段声明的小圆括号中，以选项存在作为验证提交
  2. 自定义方法，在序列化器中作为对象方法来提供验证[ 这部分验证的方法，必须以"validate_<字段>" 或者 "validate" 作为方法名 ]
  3. 自定义函数，在序列化器外部，提前声明一个验证代码，然后在字段声明的小圆括号中，通过 "validators=[验证函数１,验证函数２...]"
"""

def check_user(data):
    if data == "oldboy":
        raise serializers.ValidationError("用户名不能为oldboy！")
    return data

class Student3Serializer(serializers.Serializer):
    # 声明序列化器
    # 1. 字段声明[ 要转换的字段，当然，如果写了第二部分代码，有时候也可以不用写字段声明 ]
    name = serializers.CharField(max_length=10, min_length=4, validators=[check_user])
    sex = serializers.BooleanField(required=True)
    age = serializers.IntegerField(max_value=150, min_value=0)

    # 2. 可选[ 如果序列化器继承的是ModelSerializer，则需要声明对应的模型和字段, ModelSerializer是Serializer的子类 ]

    # 3. 可选[ 用于对客户端提交的数据进行验证 ]
    """验证单个字段值的合法性"""
    def validate_name(self, data):
        if data == "root":
            raise serializers.ValidationError("用户名不能为root！")
        return data

    def validate_age(self, data):
        if data < 18:
            raise serializers.ValidationError("年龄不能小于18")
        return data

    """验证多个字段值的合法性"""
    def validate(self, attrs):
        name = attrs.get('name')
        age = attrs.get('age')

        if name == "alex" and age == 22:
            raise serializers.ValidationError("alex在22时的故事。。。")

        return attrs

    # 4. 可选[ 用于把通过验证的数据进行数据库操作，保存到数据库 ]
    def create(self, validated_data):
        """接受客户端提交的新增数据"""
        name = validated_data.get('name')
        age = validated_data.get('age')
        sex = validated_data.get('sex')
        instance = Student.objects.create(name=name, age=age, sex=sex)
        # instance = Student.objects.create(**validated_data)
        print(instance)
        return instance

    def update(self, instance, validated_data):
        """用于在反序列化中对于验证完成的数据进行保存更新"""
        name = validated_data.get('name')
        age = validated_data.get('age')
        sex = validated_data.get('sex')
        instance.name = name
        instance.age = age
        instance.sex = sex

        instance.save()

        return instance


"""
开发中往往一个资源的序列化和反序列化阶段都是写在一个序列化器中的
所以我们可以把上面的两个阶段合并起来，以后我们再次写序列化器，则直接按照以下风格编写即可。
"""


class Student5Serializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=10, min_length=4, validators=[check_user])
    sex = serializers.BooleanField(required=True)
    age = serializers.IntegerField(max_value=150, min_value=0)
    class_null = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)

    # 2. 可选[ 如果序列化器继承的是ModelSerializer，则需要声明对应的模型和字段, ModelSerializer是Serializer的子类 ]

    # 3. 可选[ 用于对客户端提交的数据进行验证 ]
    """验证单个字段值的合法性"""
    def validate_name(self, data):
        if data == "root":
            raise serializers.ValidationError("用户名不能为root！")
        return data

    def validate_age(self, data):
        if data < 18:
            raise serializers.ValidationError("年龄不能小于18")
        return data

    """验证多个字段值的合法性"""
    def validate(self, attrs):
        name = attrs.get('name')
        age = attrs.get('age')

        if name == "alex" and age == 22:
            raise serializers.ValidationError("alex在22时的故事。。。")

        return attrs

    # 4. 可选[ 用于把通过验证的数据进行数据库操作，保存到数据库 ]
    def create(self, validated_data):
        """接受客户端提交的新增数据"""
        name = validated_data.get('name')
        age = validated_data.get('age')
        sex = validated_data.get('sex')
        instance = Student.objects.create(name=name, age=age, sex=sex)
        # instance = Student.objects.create(**validated_data)
        print(instance)
        return instance

    def update(self, instance, validated_data):
        """用于在反序列化中对于验证完成的数据进行保存更新"""
        name = validated_data.get('name')
        age = validated_data.get('age')
        sex = validated_data.get('sex')
        instance.name = name
        instance.age = age
        instance.sex = sex

        instance.save()

        return instance


"""
我们可以使用ModelSerializer来完成模型类序列化器的声明
这种基于ModelSerializer声明序列化器的方式有三个优势：
1. 可以直接通过声明当前序列化器中指定的模型中把字段声明引用过来
2. ModelSerializer是继承了Serializer的所有功能和方法，同时还编写update和create
3. 模型中同一个字段中关于验证的选项，也会被引用到序列化器中一并作为选项参与验证
"""

class StudentModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        # fields = "__all__"  # 表示引用所有字段
        fields = ["id", "name", "age", "class_null", "is_18"]  # is_18 为自定制字段，需要在models里自定义方法。
        # exclude = ["age"]  # 使用exclude可以明确排除掉哪些字段, 注意不能和fields同时使用。
        # 传递额外的参数，为ModelSerializer添加或修改原有的选项参数
        extra_kwargs = {
            "name": {"max_length": 10, "min_length": 4, "validators": [check_user]},
            "age": {"max_value": 150, "min_value": 0},
        }

    def validate_name(self, data):
        if data == "root":
            raise serializers.ValidationError("用户名不能为root！")
        return data

    def validate(self, attrs):
        name = attrs.get('name')
        age = attrs.get('age')

        if name == "alex" and age == 22:
            raise serializers.ValidationError("alex在22时的故事。。。")

        return attrs